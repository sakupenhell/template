from src.bootstrap.di.container import create_container


async def test_container_creation_and_close() -> None:
    container = create_container()
    assert container is not None
    await container.close()
