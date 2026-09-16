from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException


def test_entity_not_found_exception_message() -> None:
    exc = EntityNotFoundException("Item", 42)

    assert exc.entity_name == "Item"
    assert exc.entity_id == 42
    assert exc.message == "Item with id=42 not found"


def test_entity_already_exists_exception_message() -> None:
    exc = EntityAlreadyExistsException("Item", "duplicate-title")

    assert exc.entity_name == "Item"
    assert exc.identifier == "duplicate-title"
    assert exc.message == "Item with identifier=duplicate-title already exists"
