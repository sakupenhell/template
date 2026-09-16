import pytest

from src.application.dto.pagination import (
    PaginatedOutputDTO,
    PaginationInputDTO,
    get_limit_offset,
    get_total_pages,
)
from src.application.exceptions import BadRequestException


def test_get_limit_offset() -> None:
    assert get_limit_offset(page=1, page_size=20) == (20, 0)
    assert get_limit_offset(page=2, page_size=20) == (20, 20)
    assert get_limit_offset(page=3, page_size=10) == (10, 20)


def test_get_total_pages() -> None:
    assert get_total_pages(total=0, page_size=20) == 0
    assert get_total_pages(total=20, page_size=20) == 1
    assert get_total_pages(total=21, page_size=20) == 2


def test_pagination_input_dto() -> None:
    dto = PaginationInputDTO(page=1, page_size=20)

    assert dto.page == 1
    assert dto.page_size == 20


def test_pagination_input_dto_rejects_out_of_range_page() -> None:
    with pytest.raises(BadRequestException):
        PaginationInputDTO(page=0, page_size=20)


def test_pagination_input_dto_rejects_out_of_range_page_size() -> None:
    with pytest.raises(BadRequestException):
        PaginationInputDTO(page=1, page_size=1000)


def test_paginated_output_dto() -> None:
    output = PaginatedOutputDTO(
        items=["item1", "item2"],
        total=2,
        page=1,
        page_size=20,
        total_pages=1,
    )

    assert len(output.items) == 2
    assert output.total == 2
