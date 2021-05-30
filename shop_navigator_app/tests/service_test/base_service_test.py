import pytest
from shop_navigator_app import db
from shop_navigator_app.models.address import Address
from shop_navigator_app.models.shop import Shop
from shop_navigator_app.models.product import Product
from shop_navigator_app.schemas.address_schema import AddressSchema
from shop_navigator_app.schemas.shop_schema import ShopSchema
from shop_navigator_app.schemas.product_schema import ProductSchema
from shop_navigator_app.service.base_service import BaseService


@pytest.fixture
def data_for_instances_creation():
    return {
        'address': {
            'schema': AddressSchema,
            'data': [
                {
                    'country': 'Україна',
                    'city': 'Харків',
                    'street': 'Сумська',
                    'building': '124'
                },
                {
                    'country': 'Україна',
                    'city': 'Київ',
                    'street': 'Незалежності',
                    'building': '44А'
                }
            ]
        },
        'shop': {
            'schema': ShopSchema,
            'data': [
                {
                    'about': 'Чудовий магазин у центрі міста',
                    'address_id': 100,
                    'name': 'Сяйво'
                },
                {
                    'about': 'Найякісніше взуття міста',
                    'address_id': 100,
                    'name': 'OldNewShoes'
                }
            ]
        },
        'product': {
            'schema': ProductSchema,
            'data': [
                {
                    'label': 'Новинка',
                    'description': 'Гарний одяг',
                    'name': 'Куртка',
                    'rating': 4
                },
                {
                    'description': 'Гарний одяг',
                    'name': 'Кросівки NS Western',
                    'rating': 2
                },
                {
                    'description': 'Представник вишуканої '
                                   'колекції весняного сезону',
                    'name': 'Шпалери SmileSpring',
                    'rating': 5
                }
            ]
        }
    }


@pytest.fixture
def instances_to_insert(data_for_instances_creation):
    tested_models = data_for_instances_creation.keys()
    found_instances = dict()
    for model in tested_models:
        model_info = data_for_instances_creation[model]
        models_list = get_instances_list(
            model_info['schema'](),
            model_info['data']
        )
        found_instances[model] = models_list
    return found_instances


@pytest.fixture
def shop_address_to_insert(data_for_instances_creation):
    return get_single_instance(
        AddressSchema(),
        data_for_instances_creation['address']['data'][0]
    )


MODELS = {
    'address': Address,
    'shop': Shop,
    'product': Product
}


def get_instances_list(schema, instances_data):
    instances_list = list()
    for instance in instances_data:
        instances_list.append(
            get_single_instance(schema, instance)
        )
    return instances_list


def get_single_instance(schema, instance_data):
    return schema.load(
        instance_data, session=db.session
    )


def test_insert_select_functions(instances_to_insert, shop_address_to_insert):
    tested_models = instances_to_insert.keys()
    shop_test_address = create_test_shop_address(
        shop_address_to_insert
    )
    set_shops_address_id(shop_test_address.id, instances_to_insert['shop'])
    for model in tested_models:
        check_model_insert_select_functions(
            model, instances_to_insert
        )
    delete_instances([shop_test_address])


def create_test_shop_address(shop_address_to_insert):
    address_instance = [shop_address_to_insert]
    insert_model_instances(address_instance)
    return address_instance[0]


def set_shops_address_id(address_id, shops):
    for shop in shops:
        shop.address_id = address_id


def check_model_insert_select_functions(model_name, instances_to_insert):
    model_instances = instances_to_insert[model_name]
    current_model = MODELS[model_name]
    insert_model_instances(model_instances)
    check_insertion_correctness(model_instances, current_model)
    delete_instances(model_instances)


def insert_model_instances(model_instances):
    for model_instance in model_instances:
        BaseService.insert_new_instance(db.session, model_instance)


def check_insertion_correctness(instances, current_model):
    for instance in instances:
        found_instance = BaseService(current_model).get_first_instance_by_id(
            db.session, instance.id
        )
        assert found_instance is not None


def delete_instances(instances):
    for instance in instances:
        BaseService.delete_instance(db.session, instance)
