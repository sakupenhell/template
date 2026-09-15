from typing import Protocol, TypeVar

InputDTO = TypeVar("InputDTO", contravariant=True)
OutputDTO = TypeVar("OutputDTO", covariant=True)


class IUseCase(Protocol[InputDTO, OutputDTO]):
    async def execute(self, *, input_dto: InputDTO) -> OutputDTO | None:
        pass


class ICommand(IUseCase[InputDTO, OutputDTO], Protocol):
    pass


class IQuery(IUseCase[InputDTO, OutputDTO], Protocol):
    pass
