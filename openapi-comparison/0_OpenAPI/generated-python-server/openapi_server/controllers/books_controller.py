import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.success_response_deleted_book import SuccessResponseDeletedBook  # noqa: E501
from openapi_server.models.success_response_list_books import SuccessResponseListBooks  # noqa: E501
from openapi_server.models.success_response_single_book import SuccessResponseSingleBook  # noqa: E501
from openapi_server import util


def books_get():  # noqa: E501
    """Lấy danh sách toàn bộ sách

     # noqa: E501


    :rtype: Union[SuccessResponseListBooks, Tuple[SuccessResponseListBooks, int], Tuple[SuccessResponseListBooks, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_delete(id):  # noqa: E501
    """Xóa một cuốn sách

     # noqa: E501

    :param id: ID của cuốn sách
    :type id: int

    :rtype: Union[SuccessResponseDeletedBook, Tuple[SuccessResponseDeletedBook, int], Tuple[SuccessResponseDeletedBook, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_get(id):  # noqa: E501
    """Lấy thông tin chi tiết một cuốn sách

     # noqa: E501

    :param id: ID của cuốn sách
    :type id: int

    :rtype: Union[SuccessResponseSingleBook, Tuple[SuccessResponseSingleBook, int], Tuple[SuccessResponseSingleBook, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_put(id, body):  # noqa: E501
    """Cập nhật thông tin sách

     # noqa: E501

    :param id: ID của cuốn sách
    :type id: int
    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[SuccessResponseSingleBook, Tuple[SuccessResponseSingleBook, int], Tuple[SuccessResponseSingleBook, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Thêm một cuốn sách mới

     # noqa: E501

    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[SuccessResponseSingleBook, Tuple[SuccessResponseSingleBook, int], Tuple[SuccessResponseSingleBook, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
