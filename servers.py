#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, Union
from typing import List, Dict
from abc import ABC, abstractmethod, abstractproperty


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):

        # Sprawdzamy zgodność typów
        if not isinstance(name, str) or not isinstance(price, (float, int)):
            raise ValueError

        if re.fullmatch(r'^[a-zA-Z]+\d+$', name) is None:
            raise ValueError

        self.name: str = name
        self.price: float = float(price)

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość

    # Poniższe metody umożliwiają porówynywanie poszczególnych instancji klasy
    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __gt__(self, other):
        return self.price > other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __hash__(self):
        return hash((self.name, self.price))


# Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
class TooManyProductsFoundError(Exception):
    def __init__(self, number_of_founded_products, n_max_returned_entries,
                 message='Number of founded products exceeds the limit'):
        self.number_of_founded_products = number_of_founded_products
        self.n_max_returned_entries = n_max_returned_entries
        self.message = message

    def __str__(self):
        return self.message + ' ({0} > {1})'.format(self.number_of_founded_products, self.n_max_returned_entries)


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 3
    # ilość serwerów to zmienna dostępna dla każdej instancji klasy, tak jak n_max_returned_entries
    # i jest wykorzystywana do przydzielania id do nowego serwera
    servers_number = 0

    def __init__(self):
        self.id = self.__class__.servers_number
        self.__class__.servers_number += 1  # po powstaniu instancji klasy inkrementujemy zmienną klasową

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        search_results: List[Product] = []
        for product in self._get_products_list():
            letters_counter = 0
            numbers_counter = 0
            for sign in product.name:
                if sign.isalpha():
                    letters_counter += 1
                if sign.isdigit():
                    numbers_counter += 1
            if letters_counter == n_letters and numbers_counter in [2, 3]:
                search_results.append(product)
            if len(search_results) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(len(search_results), self.n_max_returned_entries)  # Wyrzucenie wyjątku
        return sorted(search_results)

    @abstractmethod
    def _get_products_list(self) -> List[Product]:
        raise NotImplemented


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()  # Przy konstrukcji ListServer Tworzymy też Server, który jest klasą macierzystą
        products = list(dict.fromkeys(products))  # Produkty nie mogą się powtarzać, więc usuwam duplikaty
        self.products: List[Product] = products

    def _get_products_list(self) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()
        products = list(dict.fromkeys(products))  # Produkty nie mogą się powtarzać, więc usuwam duplikaty
        self.products = {product.name: product for product in products}

    def _get_products_list(self, n_letters: int = 1) -> List[Product]:
        return [product for product in self.products.values()]


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: Server) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Union[float, None]:
        return sum(product.price for product in self.server.get_entries(n_letters))
