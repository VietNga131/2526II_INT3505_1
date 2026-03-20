import unittest

from flask import json

from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.success_response_deleted_book import SuccessResponseDeletedBook  # noqa: E501
from openapi_server.models.success_response_list_books import SuccessResponseListBooks  # noqa: E501
from openapi_server.models.success_response_single_book import SuccessResponseSingleBook  # noqa: E501
from openapi_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_books_get(self):
        """Test case for books_get

        Lấy danh sách toàn bộ sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_delete(self):
        """Test case for books_id_delete

        Xóa một cuốn sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_get(self):
        """Test case for books_id_get

        Lấy thông tin chi tiết một cuốn sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_put(self):
        """Test case for books_id_put

        Cập nhật thông tin sách
        """
        book_input = {"author":"Paulo Coelho","title":"Nhà Giả Kim"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(book_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Thêm một cuốn sách mới
        """
        book_input = {"author":"Paulo Coelho","title":"Nhà Giả Kim"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
