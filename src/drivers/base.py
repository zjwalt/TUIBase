from dataclasses import dataclass
from abc import ABC, abstractmethod

## --------------- ##
#   Data Classes    #
## --------------- ##


@dataclass
class ConnectionConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: str
    primary_key: bool
    ## Think about Foreign Key relations


@dataclass
class TableInfo:
    name: str
    schema: str | None
    columns: list[ColumnInfo]


@dataclass
class QueryResults:
    columns: list[str]
    rows: list[tuple]
    row_count: int


## --------------- ##
# Custom Exceptions #
## --------------- ##


class DriverError(Exception):
    """Base for all driver Errors"""


class DriverConnectionError(DriverError):
    """Raised when connect() fails"""


class DriverQueryError(DriverError):
    """Raised when execute_query() fails"""


## --------------- ##
#    Abstraction    #
## --------------- ##


class DatabaseDriver(ABC):
    @abstractmethod
    async def connect(self, config: ConnectionConfig) -> None:
        """Establish Connection. Raise DriverConnectionError on failure."""

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def list_schema(self) -> list[str]:
        pass

    @abstractmethod
    async def list_tables(self, schema: str | None) -> list[TableInfo]:
        pass

    @abstractmethod
    async def execute_query(self, sql: str) -> QueryResults:
        """Raise DriverQueryError on failure."""
