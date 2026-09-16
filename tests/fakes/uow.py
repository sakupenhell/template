from src.application.interfaces.uow import AbstractUOW


class FakeUOW(AbstractUOW):
    def __init__(self) -> None:
        self.created = False
        self.committed = False
        self.rolled_back = False
        self.closed = False

    async def create_transaction(self) -> None:
        self.created = True

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

    async def close_transaction(self, *exc: object) -> None:
        self.closed = True
