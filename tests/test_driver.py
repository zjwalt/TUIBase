import asyncio
from src.drivers.postgres import PostgresDriver
from src.drivers.base import ConnectionConfig


async def main():
    driver = PostgresDriver()
    config = ConnectionConfig(
        host="aws-1-us-east-1.pooler.supabase.com",
        port=6543,
        user="postgres.jfyphgxpdznacepykfkp",
        password="haR9rlsU7v1dJS5d",
        database="postgres",
    )
    await driver.connect(config)
    schema = await driver.list_schema()
    tables = await driver.list_tables("public")
    result = await driver.execute_query("SELECT * FROM players;")
    await driver.disconnect()

    print(result)


asyncio.run(main())
