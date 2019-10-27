from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, call

from databases.crud import pipeline_create_databases, s
from databases.entrance import entrance
from databases.exit import leave_the_store
from databases.get_data_for_api import get_stores, get_products_in_store, get_products_in_buying_for_customer, \
    get_quantity_for_product_customer_in_buying, get_purchases_id_from_customer, get_name_product_from_id_product, \
    get_purchases_names_from_customer, get_available_product_for_customer
from databases.purchases import take_product, return_product


class TestGetDataForApi(TestCase):
    def test_get_stores(self):
        # Given
        pipeline_create_databases()

        expected_rows_names = [("magasin de la paix", 1), ("magasin de la guerre", 2)]

        # When
        names = get_stores()

        # Then
        self.assertListEqual(expected_rows_names, names)

    def test_get_products_in_store(self):
        # Given
        pipeline_create_databases()
        id_store = 1
        expected_rows = 3

        # When
        products = get_products_in_store(id_store)

        # Then
        rows = len(products)
        self.assertEqual(expected_rows, rows)
        for id_prod, name, quantity in products:
            assert (isinstance(id_prod, int))
            assert (isinstance(name, str))
            assert (isinstance(quantity, int))

    def test_get_products_in_buying_for_customer(self):
        # Given
        pipeline_create_databases()

        id_store = 2
        id_customer = entrance(id_store, "Gimenez", "Victorien")
        take_product(id_store, id_customer, "evian 1l")
        take_product(id_store, id_customer, "KitKat paquet de 6")
        return_product(id_store, id_customer, "KitKat paquet de 6")

        expected_rows = 1

        # When
        products = get_products_in_buying_for_customer(id_store, id_customer)

        # Then
        rows = len(products)
        self.assertEqual(expected_rows, rows)
        for id_prod, name, quantity in products:
            assert (isinstance(id_prod, int))
            assert (isinstance(name, str))
            assert (isinstance(quantity, int))

    def test_get_quantity_for_product_customer_in_buying(self):
        # Given
        pipeline_create_databases()

        id_store = 2
        id_customer = entrance(id_store, "Gimenez", "Victorien")
        take_product(id_store, id_customer, "evian 1l")

        expected_quantity_evian = 1
        expected_quantity_kitkat = 0

        # When
        quantity_evian = get_quantity_for_product_customer_in_buying(id_store, id_customer, 2)
        quantity_kitkat = get_quantity_for_product_customer_in_buying(id_store, id_customer, 3)

        # Then
        self.assertEqual(expected_quantity_evian, quantity_evian)
        self.assertEqual(expected_quantity_kitkat, quantity_kitkat)

    @patch("databases.get_data_for_api.get_quantity_for_product_customer_in_buying")
    @patch("databases.get_data_for_api.get_products_in_store")
    def test_get_available_product_for_customer(self, mock_get_product_in_store,
                                                mock_get_quantity_for_product_customer):
        # Given
        id_store = 1
        id_customer = 1

        mock_get_product_in_store.return_value = [(1, 'Evian 50 cL', 2), (2, 'Evian 1L', 8), (3, 'Lait 50 cL', 12)]
        mock_get_quantity_for_product_customer.return_value = 2
        expected_calls_get_quantity = [
            call(id_store, id_customer, 1),
            call(id_store, id_customer, 2),
            call(id_store, id_customer, 3)
        ]
        expected_available = [(2, 'Evian 1L', 8), (3, 'Lait 50 cL', 12)]

        # When
        available = get_available_product_for_customer(id_store, id_customer)

        # Then
        mock_get_product_in_store.assert_called_once_with(id_store)
        mock_get_quantity_for_product_customer.has_calls(expected_calls_get_quantity)
        self.assertListEqual(expected_available, available)

    def test_get_purchases_id_from_customer(self):
        # Given
        pipeline_create_databases()
        id_store = 2
        id_customer = entrance(id_store, "Gimenez", "Victorien")
        take_product(id_store, id_customer, "evian 1l")
        leave_the_store(id_store, id_customer)
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M")

        expected_rows = 1

        # When
        purchases = get_purchases_id_from_customer(id_customer, id_store, now)

        # Then
        rows = len(purchases)
        self.assertEqual(expected_rows, rows)
        for date_purchase, id, quantity in purchases:
            assert (isinstance(date_purchase, datetime))
            assert (isinstance(id, int))
            assert (isinstance(quantity, int))

    def test_get_name_product_from_id_product(self):
        # Given
        pipeline_create_databases()

        id_product = 1

        # When
        name_product = get_name_product_from_id_product(id_product)

        # Then
        assert (isinstance(name_product, str))

    @patch("databases.get_data_for_api.get_name_product_from_id_product")
    @patch("databases.get_data_for_api.get_purchases_id_from_customer")
    def test_get_purchases_names_from_customer(self, mock_get_purchases_id, mock_get_name_product):
        # Given
        pipeline_create_databases()
        id_store = 2
        id_customer = entrance(id_store, "Gimenez", "Victorien")
        take_product(id_store, id_customer, "evian 1l")
        leave_the_store(id_store, id_customer)
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M")

        mock_get_purchases_id.return_value = [["date", "id_1", "quantity"], ["date", "id_2", "quantity"]]
        mock_get_name_product.return_value = "name"
        expected_get_name_product = [
            call("id_1"),
            call("id_2")
        ]
        expected_result = [("date", "name", "quantity"), ("date", "name", "quantity")]

        # When
        result = get_purchases_names_from_customer(id_customer, id_store, now)

        # Then
        mock_get_purchases_id.assert_called_once_with(id_customer, id_store, now)
        mock_get_name_product.has_calls(expected_get_name_product)
        self.assertListEqual(expected_result, result)
