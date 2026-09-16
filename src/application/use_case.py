from typing import Protocol


class IUseCase[InputDTO, OutputDTO](Protocol):
    async def execute(self, *, input_dto: InputDTO) -> OutputDTO: ...


class ICommand[InputDTO, OutputDTO](IUseCase[InputDTO, OutputDTO], Protocol): ...


class IQuery[InputDTO, OutputDTO](IUseCase[InputDTO, OutputDTO], Protocol): ...
