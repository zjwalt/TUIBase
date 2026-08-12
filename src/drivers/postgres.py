import asyncpg
from .base import DatabaseDriver, ConnectionConfig, DriverConnectionError


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
                "SELECT schema_name FROM information_schema.schemata"
            )
            return [record["schema_name"] for record in rows]

    async def list_tables(self) -> list[str]:
        return []

    async def execute_query(self) -> str:
        return ""
