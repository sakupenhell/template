import pytest

from tests.fakes.uow import FakeUOW


async def test_uow_success_flow() -> None:
    uow = FakeUOW()
    async with uow:
        pass

    assert uow.created is True
    assert uow.committed is True
    assert uow.rolled_back is False
    assert uow.closed is True


async def test_uow_exception_flow() -> None:
    uow = FakeUOW()
    with pytest.raises(RuntimeError):
        async with uow:
            raise RuntimeError("Simulated failure")

    assert uow.created is True
    assert uow.committed is False
    assert uow.rolled_back is True
    assert uow.closed is True
