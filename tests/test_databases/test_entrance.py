from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import and_

from databases.entrance import create_customer, customer_in_the_store, entrance
from databases.models import Customer, IsInStore
from tests.test_databases.crud_test import pipeline_create_databases_test, s


class TestEntrance(TestCase):
    def test_create_customer(self):
        # Given
        pipeline_create_databases_test()
        last_name = "B"
        first_name = "A"
        expected_new_id = s.query(Customer).count() + 1
        first_customer = s.query(Customer).first()
        s.close()
        expected_id_fist_customer = 1

        # When
        _ = create_customer(s, last_name, first_name)
        id_first_customer = create_customer(s, first_customer.last_name, first_customer.first_name)

        # Then
        id_new_customer = s.query(Customer).with_entities(Customer.id_customer).filter(
            and_(
                Customer.last_name == last_name,
                Customer.first_name == first_name
            )
        ).all()
        s.close()

        self.assertEqual(len(id_new_customer), 1)
        self.assertEqual(id_new_customer[0][0], expected_new_id)

        self.assertEqual(id_first_customer, expected_id_fist_customer)

    def test_customer_in_the_store(self):
        # Given
        pipeline_create_databases_test()
        create_customer(s, 'A', 'B')
        id_store = 1
        id_existing_customer = 1
        id_new_customer = s.query(Customer).count()
        expected_rows = s.query(IsInStore).count() + 1
        s.close()

        # When
        _ = customer_in_the_store(s, id_store, id_existing_customer)
        _ = customer_in_the_store(s, id_store, id_new_customer)

        # Then
        is_in_new_customer = s.query(IsInStore).filter(
            and_(
                IsInStore.id_store == id_store,
                IsInStore.id_customer == id_existing_customer
            )
        ).first().is_in
        rows_table = s.query(IsInStore).count()

        s.close()

        self.assertEqual(expected_rows, rows_table)
        self.assertEqual(True, is_in_new_customer)

    @patch("databases.entrance.customer_in_the_store")
    @patch("databases.entrance.create_customer")
    def test_entrance(self, mock_create_customer, mock_customer_in_store):
        # Given
        id_store = 1
        last_name = "A"
        first_name = "B"
        mail = "5"

        id_returned_create_function = 1
        mock_create_customer.return_value = id_returned_create_function

        # When
        _ = entrance(s, id_store, last_name, first_name, mail)

        # Then
        mock_create_customer.assert_called_once_with(s, last_name, first_name, mail)
        mock_customer_in_store.assert_called_once_with(s, id_store, id_returned_create_function)
