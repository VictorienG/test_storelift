from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import and_

from databases.purchases import find_id_product, same_buying, new_buying, take_product, return_product, \
    put_product_in_store

from databases.models import Product, Buying
from tests.test_databases.crud_test import pipeline_create_databases_test, s


class TestPurchases(TestCase):
    def test_find_id_product(self):
        # Given
        pipeline_create_databases_test()
        product = s.query(Product).first()
        name_product = product.name
        expected_unit_price = product.unit_price
        expected_id_product = 1
        s.close()

        # Then
        id_product, unit_price = find_id_product(s, name_product)

        # When
        self.assertEqual(expected_id_product, id_product)
        self.assertEqual(expected_unit_price, unit_price)
        s.close()

    def test_new_buying(self):
        # Given
        pipeline_create_databases_test()
        id_store = 1
        product = s.query(Product).first()
        id_product = product.id_product
        name = product.name
        id_customer = 1
        unit_price = 1.1

        expected_rows = s.query(Buying).count() + 1
        expected_quantity = 1
        s.close()

        # When
        _ = new_buying(s, id_store, id_customer, id_product, name, unit_price)

        # Then
        rows = s.query(Buying).count()
        quantity = s.query(Buying).filter(
            and_(
                Buying.id_store == id_store,
                Buying.id_customer == id_customer,
                Buying.id_prod == id_product
            )
        ).first().quantity
        s.close()

        self.assertEqual(expected_rows, rows)
        self.assertEqual(expected_quantity, quantity)

    def test_same_buying(self):
        # Given
        pipeline_create_databases_test()
        id_store = 1
        product = s.query(Product).first()
        id_product = product.id_product
        name = product.name
        id_customer = 1
        expected_quantity = 2
        unit_price = 1
        new_buying(s, id_store, id_customer, id_product, name, unit_price)

        # When
        _ = same_buying(s, id_store, id_customer, id_product)

        # Then
        quantity = s.query(Buying).filter(
            and_(
                Buying.id_store == id_store,
                Buying.id_customer == id_customer,
                Buying.id_prod == id_product
            )
        ).first().quantity
        s.close()
        self.assertEqual(expected_quantity, quantity)

    def test_put_product_in_store(self):
        pipeline_create_databases_test()
        id_store = 1
        product = s.query(Product).first()
        id_product = product.id_product
        name = product.name
        id_customer = 1
        expected_quantity = 0
        unit_price = 1
        new_buying(s, id_store, id_customer, id_product, name, unit_price)

        # When
        _ = put_product_in_store(s, id_store, id_customer, id_product)

        # Then
        quantity = s.query(Buying).filter(
            and_(
                Buying.id_store == id_store,
                Buying.id_customer == id_customer,
                Buying.id_prod == id_product
            )
        ).first().quantity
        s.close()
        self.assertEqual(expected_quantity, quantity)

    @patch("databases.purchases.same_buying")
    @patch("databases.purchases.find_id_product")
    def test_take_product_try(self, mock_id_product, mock_same_product):
        # Given
        name_product = "A"
        id_store = 1
        id_customer = 1

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = take_product(s, id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(s, name_product)
        mock_same_product.assert_called_once_with(s, id_store, id_customer, id_product)

    @patch("databases.purchases.new_buying")
    @patch("databases.purchases.find_id_product")
    def test_take_product_except(self, mock_id_product, mock_new_product):
        # Given
        name_product = "A"
        id_store = 10
        id_customer = 1

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = take_product(s, id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(s, name_product)
        mock_new_product.assert_called_once_with(s, id_store, id_customer, id_product, name_product, unit_price)

    @patch("databases.purchases.put_product_in_store")
    @patch("databases.purchases.find_id_product")
    def test_return_product(self, mock_id_product, mock_put_product):
        # Given
        id_store = 1
        id_customer = 1
        name_product = "A"

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = return_product(s, id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(s, name_product)
        mock_put_product.assert_called_once_with(s, id_store, id_customer, id_product)
