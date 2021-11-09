import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

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

class ProductTest(unittest.TestCase):

    def test_right_name(self):
        product = Product('wod55', 100)
        self.assertEqual(100, product.price)
        self.assertEqual('wod55', product.name)

    def test_wrong_name(self):
        with self.assertRaises(ValueError):
            Product('wod55www', 100)




if __name__ == '__main__':
    unittest.main()