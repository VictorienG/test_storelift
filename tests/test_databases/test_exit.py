from unittest import TestCase
from unittest.mock import patch, call

from sqlalchemy import and_

from databases.purchases import take_product
from databases.entrance import entrance
from databases.exit import change_stock, compute_total_price, put_in_history, delete_purchases_customer, \
    change_to_false_in_is_in_store, leave_the_store
from databases.models import Stock, HistoryCustomer, Buying, IsInStore
from tests.test_databases.crud_test import pipeline_create_databases_test, s


class TestExit(TestCase):
    def test_change_stock(self):
        # Given
        pipeline_create_databases_test()
        product = s.query(Stock).first()
        id_store = product.id_store
        id_product = product.id_prod
        quantity = product.quantity
        quantity_bought = 2

        expected_quantity = quantity - quantity_bought

        # When
        change_stock(s, id_store, id_product, quantity_bought)

        # Then
        final_quantity = s.query(Stock).filter(
            and_(
                Stock.id_store == id_store,
                Stock.id_prod == id_product
            )
        ).first().quantity
        self.assertEqual(expected_quantity, final_quantity)

    def test_compute_total_price(self):
        # Given
        s.close()
        pipeline_create_databases_test()

        id_store = 2
        id_customer = entrance(s, id_store, "Gimenez", "Victorien")
        take_product(s, id_store, id_customer, "evian 1l")
        take_product(s, id_store, id_customer, "evian 1l")

        price_evian_1l = 1
        quantity_evian_1l = 2
        id_evian_1l = 2
        expected_total_price = price_evian_1l * quantity_evian_1l
        expected_products_bought = [[id_evian_1l, quantity_evian_1l]]

        # When
        total_price, products_bought = compute_total_price(s, id_store, id_customer)
        s.close()

        # Then
        self.assertEqual(float(expected_total_price), float(total_price))
        self.assertListEqual(expected_products_bought, products_bought)

    def test_put_in_history(self):
        # Given
        pipeline_create_databases_test()
        id_store = 2
        id_customer = entrance(s, id_store, "Gimenez", "Victorien")
        take_product(s, id_store, id_customer, "evian 1l")
        take_product(s, id_store, id_customer, "KitKat paquet de 6")

        expected_rows = 2

        # When
        _ = put_in_history(s, id_store, id_customer)

        # Then
        rows = s.query(HistoryCustomer).count()
        self.assertEqual(expected_rows, rows)
        s.close()

    def test_delete_purchases_customer(self):
        # Given
        pipeline_create_databases_test()
        id_store = 2
        id_customer = entrance(s, id_store, "Gimenez", "Victorien")
        take_product(s, id_store, id_customer, "evian 1l")
        take_product(s, id_store, id_customer, "KitKat paquet de 6")

        expected_rows = 0

        # When
        _ = delete_purchases_customer(s, id_store, id_customer)

        # Then

        rows = s.query(Buying).count()
        self.assertEqual(expected_rows, rows)
        s.close()

    def test_change_to_false_in_is_in_store(self):
        # Given
        s.close()
        pipeline_create_databases_test()
        id_store = 2
        id_customer = entrance(s, id_store, "Gimenez", "Victorien")

        # When
        _ = change_to_false_in_is_in_store(s, id_store, id_customer)

        # Then
        is_in = s.query(IsInStore).filter(
            and_(
                IsInStore.id_customer == id_customer,
                IsInStore.id_store == id_store
            )
        ).first().is_in
        self.assertEqual(is_in, False)
        s.close

    @patch("databases.exit.change_to_false_in_is_in_store")
    @patch("databases.exit.delete_purchases_customer")
    @patch("databases.exit.put_in_history")
    @patch("databases.exit.change_stock")
    @patch("databases.exit.compute_total_price")
    def test_leave_the_store(self, mock_total_price, mock_change_stock, mock_put_in_history, mock_delete,
                             mock_change_false):
        # Given
        id_store = 1
        id_customer = 2
        total_price = 1
        purchases = [[1, 2], [3, 1]]

        mock_total_price.return_value = total_price, purchases
        expected_calls_change_stock = [
            call(s, id_store, purchases[0][0], purchases[0][1]),
            call(s, id_store, purchases[1][0], purchases[1][1])
        ]

        # When
        _ = leave_the_store(s, id_store, id_customer)

        # Then
        mock_total_price.assert_called_once_with(s, id_store, id_customer)
        mock_change_stock.has_calls(expected_calls_change_stock)
        mock_put_in_history.assert_called_once_with(s, id_store, id_customer)
        mock_delete.assert_called_once_with(s, id_store, id_customer)
        mock_change_false.assert_called_once_with(s, id_store, id_customer)
