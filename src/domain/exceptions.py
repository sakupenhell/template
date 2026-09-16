class DomainException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class EntityNotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: object) -> None:
        super().__init__(f"{entity_name} with id={entity_id} not found")
        self.entity_name = entity_name
        self.entity_id = entity_id


class EntityAlreadyExistsException(DomainException):
    def __init__(self, entity_name: str, identifier: object) -> None:
        super().__init__(f"{entity_name} with identifier={identifier} already exists")
        self.entity_name = entity_name
        self.identifier = identifier


class DomainValidationException(DomainException): ...
