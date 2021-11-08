#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, Union
from typing import List, Dict
from abc import ABC, abstractmethod, abstractproperty


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):

        # Sprawdzamy zgodność typów
        if not isinstance(name, str) or not isinstance(price, (float, int)):
            raise ValueError

        # Nie wiem co to było, więc zostawiam na razie
        # if re.fullmatch('[a-zA-Z][0-9]', name) is None: # FIXME: No nie działa mi to na razie :(((((((((((((((
        #     raise ValueError
        # Sprawdzam czy po cyfrze nie pojawia się znak
        for i in range(len(name) - 1):
            if name[i].isdigit() and name[i + 1].isalpha():
                raise ValueError
        # Tutaj bardzo 'pythonic' mi wyszło sprawdzenie czy ma co najmniej jeden znak i cyfrę
        contains_number = True if True in [sign.isdigit() for sign in name] else False
        contains_alpha = True if True in [sign.isalpha() for sign in name] else False
        contains_other_sign = True if True in [not sign.isalnum() for sign in name] else False
        if not contains_alpha or not contains_number or contains_other_sign:
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
#Fixme Nieskończone!!!
class TooManyProductsFoundError(Exception):
    def __init__(self, number_of_founded_products, message='kkk'):
        self.number_of_founded_products = number_of_founded_products
        self.message = message

    def __str__(self):
        return ''

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 5
    # ilość serwerów to zmienna dostępna dla każdej instancji klasy, tak jak n_max_returned_entries
    # i jest wykorzystywana do przydzielania id do nowego serwera
    servers_number = 0

    def __init__(self):
        self.id = self.__class__.servers_number
        self.__class__.servers_number += 1  # po powstaniu instancji klasy inkrementujemy zmienną klasową

    @abstractmethod
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pass


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()  # Przy konstrukcji ListServer Tworzymy też Server, który jest klasą macierzystą
        products = list(dict.fromkeys(products))  # Produkty nie mogą się powtarzać, więc usuwam duplikaty
        self.products: List[Product] = products

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        search_results: List[Product] = []
        for product in self.products:
            letters_counter = 0
            numbers_counter = 0
            for sign in product.name:
                if sign.isalpha():
                    letters_counter += 1
                if sign.isdigit():
                    numbers_counter += 1
            if letters_counter == n_letters and numbers_counter in [2, 3]:
                search_results.append(product)
        return qsort_products(search_results)


class MapServer:
    def __init__(self, products: List[Product]):
        # self.products = {product.name: product.price for product in products}
        # W treści zadania jest, że nazwa to klucz a wartość obiekt Product nie??
        super().__init__()
        products = list(dict.fromkeys(products))  # Produkty nie mogą się powtarzać, więc usuwam duplikaty
        self.products = {product.name: product for product in products}

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        search_results: List[Product] = []
        for product in self.products:
            letters_counter = 0
            numbers_counter = 0
            for sign in product:
                if sign.isalpha():
                    letters_counter += 1
                if sign.isdigit():
                    numbers_counter += 1
            if letters_counter == n_letters and numbers_counter in [2, 3]:
                search_results.append(self.products.get(product))
        return qsort_products(search_results)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    server: Server

    def __init__(self, server: Server) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Union[float, None]:
        try:
            return sum(product.price for product in self.server.get_entries(n_letters))
        except:
            raise TooManyProductsFoundError


def qsort_products(products: List[Product], start: int = 0, stop: int = -1) -> List[Product]:
    if stop == -1:
        stop = len(products) - 1
    i = start
    j = stop
    pivot = products[start]
    while i < j:
        while products[i] < pivot:
            i += 1
        while products[j] > pivot:
            j -= 1
        if i <= j:
            products[i], products[j] = products[j], products[i]
            i += 1
            j -= 1
    if start < j:
        qsort_products(products, start, j)
    if i < stop:
        qsort_products(products, i, stop)
    return products
