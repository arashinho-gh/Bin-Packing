from abc import ABC, abstractmethod
from . import WeightStream, WeightSet, Solution


class BinPacker(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.num_of_compares = \
            self.num_of_bins_created =\
            self.num_of_times_checked_bins = 0

    def getMetric(self, metric_name: str):
        if metric_name == 'num_of_compares':
            return self.num_of_compares
        elif metric_name == 'num_of_bins_created':
            return self.num_of_bins_created
        elif metric_name == 'num_of_times_checked_bins':
            return self.num_of_times_checked_bins


class Online(BinPacker):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, ws: WeightStream):
        capacity, stream = ws
        self.num_of_compares = \
            self.num_of_bins_created = \
            self.num_of_times_checked_bins = 0

        return self._process(capacity, stream)

    @abstractmethod
    def _process(self, c: int, stream) -> Solution:
        pass


class Offline(BinPacker):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, ws: WeightSet):
        capacity, weights = ws
        self.num_of_compares = \
            self.num_of_bins_created =\
            self.num_of_times_checked_bins = 0

        return self._process(capacity, weights)

    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Solution:
        pass
