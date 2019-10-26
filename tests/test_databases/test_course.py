from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import and_

from databases.course import find_id_product, same_buying, new_buying, take_product, return_product, \
    put_product_in_store
from databases.crud import s, pipeline_create_databases
from databases.models import Stock, Product, Buying


class TestCourse(TestCase):
    def test_find_id_product(self):
        # Given
        pipeline_create_databases()
        product = s.query(Product).first()
        name_product = product.name
        expected_unit_price = product.unit_price
        expected_id_product = 1
        s.close()

        # Then
        id_product, unit_price = find_id_product(name_product)

        # When
        self.assertEqual(expected_id_product, id_product)
        self.assertEqual(expected_unit_price, unit_price)
        s.close()

    def test_new_buying(self):
        # Given
        pipeline_create_databases()
        id_store = 1
        id_product = 1
        id_customer = 1
        unit_price = 1.1

        expected_rows = s.query(Buying).count() + 1
        expected_quantity = 1
        s.close()

        # When
        _ = new_buying(id_store, id_customer, id_product, unit_price)

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
        pipeline_create_databases()
        id_store = 1
        id_product = 1
        id_customer = 1
        expected_quantity = 2
        unit_price = 1
        new_buying(id_store, id_customer, id_product, unit_price)

        # When
        _ = same_buying(id_store, id_customer, id_product)

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
        pipeline_create_databases()
        id_store = 1
        id_product = 1
        id_customer = 1
        expected_quantity = 0
        unit_price = 1
        new_buying(id_store, id_customer, id_product, unit_price)

        # When
        _ = put_product_in_store(id_store, id_customer, id_product)

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

    @patch("databases.course.same_buying")
    @patch("databases.course.find_id_product")
    def test_take_product_try(self, mock_id_product, mock_same_product):
        # Given
        name_product = "A"
        id_store = 1
        id_customer = 1

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = take_product(id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(name_product)
        mock_same_product.assert_called_once_with(id_store, id_customer, id_product)

    @patch("databases.course.new_buying")
    @patch("databases.course.find_id_product")
    def test_take_product_except(self, mock_id_product, mock_new_product):
        # Given
        name_product = "A"
        id_store = 10
        id_customer = 1

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = take_product(id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(name_product)
        mock_new_product.assert_called_once_with(id_store, id_customer, id_product, unit_price)

    @patch("databases.course.put_product_in_store")
    @patch("databases.course.find_id_product")
    def test_return_product(self, mock_id_product, mock_put_product):
        # Given
        id_store = 1
        id_customer = 1
        name_product = "A"

        id_product = 1
        unit_price = 1
        mock_id_product.return_value = id_product, unit_price

        # When
        _ = return_product(id_store, id_customer, name_product)

        # Then
        mock_id_product.assert_called_once_with(name_product)
        mock_put_product.assert_called_once_with(id_store, id_customer, id_product)