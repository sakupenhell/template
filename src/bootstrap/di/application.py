from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection

from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_cases.commands.item.create import CreateItemCommand
from src.application.use_cases.commands.item.delete import DeleteItemCommand
from src.application.use_cases.commands.item.update import UpdateItemCommand
from src.application.use_cases.queries.item.get_by_id import GetItemByIdQuery
from src.application.use_cases.queries.item.list_items import ListItemsQuery
from src.infrastructure.database.storages.item import ItemStorage


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def item_storage(self, connection: AsyncConnection) -> IItemStorage:
        return ItemStorage(connection=connection)

    @provide
    def create_item_command(
        self,
        uow: AbstractUOW,
        item_storage: IItemStorage,
    ) -> CreateItemCommand:
        return CreateItemCommand(uow=uow, item_storage=item_storage)

    @provide
    def update_item_command(
        self,
        uow: AbstractUOW,
        item_storage: IItemStorage,
    ) -> UpdateItemCommand:
        return UpdateItemCommand(uow=uow, item_storage=item_storage)

    @provide
    def delete_item_command(
        self,
        uow: AbstractUOW,
        item_storage: IItemStorage,
    ) -> DeleteItemCommand:
        return DeleteItemCommand(uow=uow, item_storage=item_storage)

    @provide
    def get_item_by_id_query(
        self,
        uow: AbstractUOW,
        item_storage: IItemStorage,
    ) -> GetItemByIdQuery:
        return GetItemByIdQuery(uow=uow, item_storage=item_storage)

    @provide
    def list_items_query(
        self,
        uow: AbstractUOW,
        item_storage: IItemStorage,
    ) -> ListItemsQuery:
        return ListItemsQuery(uow=uow, item_storage=item_storage)
