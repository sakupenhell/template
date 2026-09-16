from dataclasses import dataclass

from src.application.constants.pagination import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE,
    MAX_PAGE_SIZE,
    MIN_PAGE,
    MIN_PAGE_SIZE,
)
from src.application.exceptions import BadRequestException


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginationInputDTO:
    page: int = MIN_PAGE
    page_size: int = DEFAULT_PAGE_SIZE

    def __post_init__(self) -> None:
        if not MIN_PAGE <= self.page <= MAX_PAGE:
            raise BadRequestException(f"page must be between {MIN_PAGE} and {MAX_PAGE}")
        if not MIN_PAGE_SIZE <= self.page_size <= MAX_PAGE_SIZE:
            raise BadRequestException(
                f"page_size must be between {MIN_PAGE_SIZE} and {MAX_PAGE_SIZE}"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedOutputDTO[ItemT]:
    items: list[ItemT]
    total: int
    page: int
    page_size: int
    total_pages: int


def get_limit_offset(page: int, page_size: int) -> tuple[int, int]:
    limit = page_size
    offset = (page - 1) * page_size
    return limit, offset


def get_total_pages(*, total: int, page_size: int) -> int:
    return -(-total // page_size) if total else 0
