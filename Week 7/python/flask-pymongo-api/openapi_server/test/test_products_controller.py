import unittest

from flask import json

from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server.models.success_response_deleted_product import SuccessResponseDeletedProduct  # noqa: E501
from openapi_server.models.success_response_list_products import SuccessResponseListProducts  # noqa: E501
from openapi_server.models.success_response_single_product import SuccessResponseSingleProduct  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_products_get(self):
        """Test case for products_get

        Lấy danh sách toàn bộ sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_delete(self):
        """Test case for products_id_delete

        Xóa sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/products/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_get(self):
        """Test case for products_id_get

        Lấy chi tiết sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/products/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_put(self):
        """Test case for products_id_put

        Cập nhật sản phẩm
        """
        product_input = {"price":2000,"name":"MacBook Pro M3","category":"Electronics"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_post(self):
        """Test case for products_post

        Thêm sản phẩm mới
        """
        product_input = {"price":2000,"name":"MacBook Pro M3","category":"Electronics"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
