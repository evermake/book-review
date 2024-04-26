import asyncio
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import AsyncGenerator, Hashable
from contextlib import asynccontextmanager
from typing import Deque, Generic, TypeVar

import aiosqlite
import yoyo


def in_memory_connection_supplier() -> aiosqlite.Connection:
    return aiosqlite.connect(":memory:")


def apply_migrations(db: str) -> None:
    backend = yoyo.get_backend(db)
    migrations = yoyo.read_migrations("book_review/migrations/")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


T = TypeVar("T", bound=Hashable)


class ResourcePool(ABC, Generic[T]):
    _max_resources: int
    _request_lock: asyncio.Lock
    _resource_returned: asyncio.Condition
    _pool: Deque[T]
    _n_resources_created: int
    _in_use: set[T]

    def __init__(self, max_resources: int):
        if max_resources < 1:
            raise ValueError(f"Invalid max_resources argument: {max_resources}")

        self._max_resources = max_resources
        self._request_lock = asyncio.Lock()
        self._resource_returned = asyncio.Condition()
        self._pool = deque()
        self._n_resources_created = 0
        self._in_use = set()

    async def close(self) -> None:
        """Close all resources."""

        async with self._request_lock:
            while self._pool:
                res = self._pool.popleft()

                await self.close_resource(res)

            while self._in_use:
                res = self._in_use.pop()

                await self.close_resource(res)

    @abstractmethod
    async def close_resource(self, res: T) -> None:
        pass

    @abstractmethod
    async def create_resource(self) -> T:
        pass

    async def get_resource(self, timeout: int = 10) -> T:
        while True:
            async with self._request_lock:
                if self._pool:
                    res = self._pool.popleft()
                    self._in_use.add(res)

                    return res

                # Can we create another resource?
                if self._n_resources_created < self._max_resources:
                    self._n_resources_created += 1
                    res = await self.create_resource()
                    self._in_use.add(res)

                    return res

                # We must wait for a resource to be returned
                async def wait_for_resource() -> None:
                    async with self._resource_returned:
                        await self._resource_returned.wait()

                try:
                    await asyncio.wait_for(wait_for_resource(), timeout=timeout)
                    # The pool now has at least one resource available and
                    # we will succeed on next iteration.
                except asyncio.TimeoutError:
                    raise RuntimeError("Timeout: No available resource in the pool.")

    async def release_resource(self, res: T) -> None:
        if res not in self._in_use:
            raise Exception("Releasing unknown object")
        # Could raise exception if two threads are releasing the same resource:
        self._in_use.remove(res)
        self._pool.append(res)

        # If someone is waiting for a resource:
        async with self._resource_returned:
            self._resource_returned.notify()

    @asynccontextmanager
    async def resource(self, timeout: int = 10) -> AsyncGenerator[T, None]:
        res = await self.get_resource(timeout)

        try:
            yield res
        finally:
            await self.release_resource(res)


class ConnectionPool(ResourcePool[aiosqlite.Connection]):
    _database: str

    def __init__(self, database: str, *, max_connections: int = 10) -> None:
        super().__init__(max_connections)
        self._database = database

    async def create_resource(self) -> aiosqlite.Connection:
        return await aiosqlite.connect(self._database, loop=asyncio.get_running_loop())

    async def release_resource(self, res: aiosqlite.Connection) -> None:
        await res.rollback()

        await super().release_resource(res)

    async def close_resource(self, res: aiosqlite.Connection) -> None:
        await res.close()
