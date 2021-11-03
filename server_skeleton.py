#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from typing import List, Dict


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    def __init__(self, _products: List):
        self._products = _products

    pass


class MapServer:
    def __init__(self, _products: Dict):
        self._products = _products

    pass


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, _server_id) -> None:
        self._server_id = _server_id

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try

            return
        except
            TooManyProductsFoundError
            return None
    pass
class Server:
    def __init__(self, id: int, n_max_returned_entries: int):
        self.id = id
        self.n_max_returned_entries = n_max_returned_entries
    pass

