import asyncpg
from .base import (
    DatabaseDriver,
    ConnectionConfig,
    DriverConnectionError,
    DriverQueryError,
    ColumnInfo,
    QueryResults,
    TableInfo,
)


class PostgresDriver(DatabaseDriver):
    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None

    async def connect(self, config: ConnectionConfig) -> None:
        try:
            self._pool = await asyncpg.create_pool(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                database=config.database,
                statement_cache_size=0,
            )
        except Exception as e:
            raise DriverConnectionError(f"Failed to connect: {e}") from e

    async def disconnect(self) -> None:
        if self._pool is not None:
            try:
                await self._pool.close()
            except Exception:
                pass
                ## TODO: Add logging later
            finally:
                self._pool = None

    async def list_schema(self) -> list[str]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT schema_name FROM information_schema.schemata;"
            )
            return [record["schema_name"] for record in rows]

    async def list_tables(self, schema) -> list[TableInfo]:
        list_tables = []
        async with self._pool.acquire() as conn:
            tables = await conn.fetch(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = $1",
                schema,
            )
            table_info = await conn.fetch(
                "SELECT table_name, column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema = $1;",
                schema,
            )

            columns_by_table: dict[str, list[ColumnInfo]] = {
                t["table_name"]: [] for t in tables
            }

            for entry in table_info:
                column = ColumnInfo(
                    name=entry["column_name"],
                    data_type=entry["data_type"],
                    nullable=entry["is_nullable"],
                )

                columns_by_table[entry["table_name"]].append(column)

            list_tables = [
                TableInfo(name=table, schema="public", columns=columns_by_table[table])
                for table in columns_by_table.keys()
            ]

        return list_tables

    async def execute_query(self, sql: str) -> QueryResults:
        try:
            command = sql.strip().split()[0].upper()
            async with self._pool.acquire() as conn:
                if command == "SELECT":
                    result = await conn.fetch(
                        sql.rstrip().rstrip(";") + " ORDER BY id;"
                        if "ORDER BY" not in sql.upper()
                        else sql
                    )

                    if len(result) > 0:
                        query_results = QueryResults(
                            columns=list(result[0].keys()),
                            rows=[tuple(row.values()) for row in result],
                            row_count=len(result),
                        )
                    else:
                        query_results = QueryResults(columns=[], rows=[], row_count=0)
                else:
                    result = await conn.execute(sql)
                    print(result)
                    query_results = QueryResults(
                        columns=[], rows=[], row_count=int(result.strip().split()[-1])
                    )

                return query_results

        except Exception as e:
            raise DriverQueryError(
                f"Failed to execute query: '{sql}'\n{'-' * 10}\nError Message: {e}\n"
            ) from e
