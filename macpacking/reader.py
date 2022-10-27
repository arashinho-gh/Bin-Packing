from abc import ABC, abstractmethod
from fileinput import filename
from os import path
from random import shuffle, seed
from typing import Any
from . import WeightSet, WeightStream


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())
    
    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline())
            capacity: int = int(reader.readline())
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)
        
class JburkardtReader():
    
    def __init__(self, files : list[str]) -> None:
        self.__files = []
        for filename in files:   
            if not path.exists("./_datasets/jburkardt/" + filename):
                raise ValueError(f'Unkown file [{filename}]')
            self.__files.append(filename)
        ''' Contains all the data from the files (capacity, solution, weights) '''
        self.data = {"capacity": None, "weights": None, "solution" : None}

    def _load_data_from_disk(self) -> WeightSet:
        for filename in self.__files:
            with open("./_datasets/jburkardt/" + filename, 'r') as reader:
                ''' get file type (c, w, s)'''
                data_type = filename.split("_")[-1].split(".")[0]

                file_data = []
                ''' gets the first line '''
                line = reader.readline().strip()
                if data_type == "c":
                    self.data["capacity"] = int(line)
                ''' gets all the data at each line and stops when we reach an empty line '''
                while len(line) > 0:
                    file_data.append(int(line))
                    line = reader.readline().strip()
                

                if data_type == "w":
                    self.data["weights"] = file_data
                elif data_type == "s":
                    self.data["solution"] = file_data
                
        return self.data

