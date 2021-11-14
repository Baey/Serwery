import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_if_get_entries_raises_an_error(self):
        products = [Product('Pyyy11', 1), Product('PyUi239', 2), Product('Pyso26', 7), Product('Pyss26', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(4)

    def test_if_products_are_unique(self):
        products = [Product('Pwo12', 1), Product('PP234', 2), Product('PP235', 1), Product('Pwo12', 1)]
        for server_type in server_types:
            server = server_type(products)
            self.assertEqual(3, len(server.products))

    def test_get_product_list(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1), Product('Pwo12', 1)]
        for server_type in server_types:
            server = server_type(products)
            self.assertEqual(server._get_products_list(), products)


class ClientTest(unittest.TestCase):

    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_None_return_1(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('Pppp237', 5)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(3))

    def test_total_price_for_None_return_2(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PP236', 50), Product('PP237', 60)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


class ProductTest(unittest.TestCase):

    def test_normal_name(self):
        product = Product('wod55', 100)
        self.assertEqual(100, product.price)
        self.assertEqual('wod55', product.name)

    def test_wrong_name(self):
        with self.assertRaises(ValueError):
            Product('wod55www', 100)


if __name__ == '__main__':
    unittest.main()
