from shop_navigator_app import app
import http
import pytest
from unittest.mock import patch
from shop_navigator_app.schemas.product_schema \
    import ProductSchema
from shop_navigator_app import db

CLIENT = app.test_client()


@pytest.fixture
def product_data_to_post():
    return {
        'correct_data': [
            {
                'name': 'Furniture World',
                'description': 'about shop',
                'rating': 3,
                'label': 'new'
            },
            {
                'name': 'Awesome clothes',
                'description': 'about shop',
                'rating': 5
            }
        ],
        'incorrect_data': [
            {
                'name': 'Furniture World'
            },
            {
                'name': 'Awesome clothes',
                'description': 'about shop',
                'rating': 11
            },
            {
                'name': 'Furniture World',
                'description': 'about shop',
                'label': 'new'
            }
        ]
    }


@pytest.fixture
def address_data_to_patch():
    return {
        'correct_data': [
            {
                'street': 'Сумська',
                'building': '15A'
            }
        ],
        'incorrect_data': [
            {
                'building': '16',
                'flat': 23
            }
        ]
    }


def test_get_request():
    with patch('shop_navigator_app.db.session.query') as _:
        all_shops_response = CLIENT.get('/product')
        assert all_shops_response.status_code == http.HTTPStatus.OK

        single_shop_response = CLIENT.get(f'/shop/1')
        assert single_shop_response.status_code == http.HTTPStatus.OK \
               or single_shop_response.status_code == http.HTTPStatus.NOT_FOUND


def test_post_request(product_data_to_post):
    check_insertion_request_correctness(
        CLIENT.post, product_data_to_post, http.HTTPStatus.CREATED,
    )


def test_put_request(product_data_to_post):
    check_method_with_incorrect_id(CLIENT.put)
    check_insertion_request_correctness(
        CLIENT.put, product_data_to_post, http.HTTPStatus.OK,
    )


def check_insertion_request_correctness(
        method, product_data_to_post, expected_positive_response
):
    with patch('shop_navigator_app.db.session.add') as _:
        with patch('shop_navigator_app.db.session.commit') as _:
            check_product_data_list(
                product_data_to_post['incorrect_data'],
                http.HTTPStatus.BAD_REQUEST,
                method
            )
            check_product_data_list(
                product_data_to_post['correct_data'],
                expected_positive_response,
                method
            )


def check_method_with_incorrect_id(method):
    with patch(
            'shop_navigator_app.service.base_service.'
            'BaseService.get_first_instance_by_id'
    ) as incorrect_id_mock:
        handle_request_with_incorrect_id(incorrect_id_mock, method)


def handle_request_with_incorrect_id(mock, method):
    mock.return_value = None
    all_shops_response = method('/product/1', json={})
    assert all_shops_response.status_code == http.HTTPStatus.NOT_FOUND


def check_product_data_list(data_list, expected_response, method):
    for data in data_list:
        with patch(
                'shop_navigator_app.service.base_service.'
                'BaseService.get_first_instance_by_id'
        ) as correct_id_mock:
            request_string = '/product'
            if method == CLIENT.put:
                if expected_response >= 400:
                    correct_id_mock.return_value = data
                else:
                    correct_id_mock.return_value = ProductSchema().load(
                        data, session=db.session
                    )
                request_string += '/1'

            new_product_response = method(request_string, json=data)
            assert new_product_response.status_code == expected_response

            if 200 <= new_product_response.status_code < 300:
                new_product_response_json = new_product_response.json
                new_product_response_json.pop('id', None)
                if 'label' not in data:
                    data['label'] = None
                assert new_product_response_json == data


def test_patch_request(address_data_to_patch):
    check_patch_with_incorrect_id()
    check_patch_with_correct_id(address_data_to_patch)


def check_patch_with_incorrect_id():
    with patch(
            'shop_navigator_app.service.base_service.'
            'BaseService.get_all_instances_by_id'
    ) as incorrect_id_mock:
        handle_request_with_incorrect_id(incorrect_id_mock, CLIENT.patch)


def check_patch_with_correct_id(address_data_to_patch):
    check_addresses_list(
        address_data_to_patch['incorrect_data'],
        http.HTTPStatus.BAD_REQUEST
    )
    check_addresses_list(
        address_data_to_patch['correct_data'],
        http.HTTPStatus.OK
    )


def check_addresses_list(data_list, expected_response):
    with patch(
            'shop_navigator_app.service.base_service.'
            'BaseService.get_all_instances_by_id'
    ) as _:
        with patch(
                'shop_navigator_app.service.base_service.'
                'BaseService.update_instance'
        ) as _:
            for address in data_list:
                response = CLIENT.patch('/address/1', json=address)
                assert response.status_code == expected_response


def test_delete_request():
    check_method_with_incorrect_id(CLIENT.delete)


def check_delete_with_correct_id():
    with patch(
            'shop_navigator_app.service.base_service.'
            'BaseService.delete_instance'
    ):
        response = CLIENT.delete('/address/1')
        assert response.status_code == 204
        assert response.json == {}
