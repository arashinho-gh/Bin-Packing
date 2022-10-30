from abc import ABC, abstractmethod
from typing import Iterator
from . import WeightStream, WeightSet, Solution


class BinPacker(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.num_of_compares = self.num_of_bins_created = self.num_of_times_checked_bins = 0



class Online(BinPacker):
    
    def __init__(self) -> None:
        super().__init__()
        
    def __call__(self, ws: WeightStream):
        capacity, stream = ws
        return self._process(capacity, stream)

    @abstractmethod
    def _process(self, c: int, stream: Iterator[int]) -> Solution:
        pass


class Offline(BinPacker):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, ws: WeightSet):
        capacity, weights = ws
        return self._process(capacity, weights)


    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Solution:
        pass
