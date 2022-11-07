from abc import ABC, abstractmethod
from fileinput import filename
from os import path
from random import shuffle, seed
from typing import Any
from . import WeightSet, WeightStream, NomralizedWeightSet


class DatasetReader(ABC):

    def offline(self):
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        
        return (capacity, weights)

    def online(self, normalize = False):
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()
        if normalize:   #nomralize the dataset if the normalize paramater is set to true
            dataset = Normalized_reading(capacity,weights)
            (capacity,weights) = dataset.Normalize()
        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one
        return (capacity, iterator())
    
    @abstractmethod
    def _load_data_from_disk(self):
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
        
class JburkardtReader(DatasetReader):
    
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
                
        return (self.data['capacity'], self.data['weights'])

class Normalized_reading():
    '''Read problem description according to the BinPP format'''
    def __init__(self, capacity ,weights: WeightStream) -> None:
        self.weights=[]
        for weight in weights:
            self.weights.append([weight])
        self.capacity = capacity
    def Normalize(self) -> NomralizedWeightSet:
            for i in range(len(self.weights)):
                if self.weights[i][0] >= self.capacity//2:
                    self.weights[i].append("A")
                elif self.weights[i][0] < self.capacity*1//2 and self.weights[i][0] >= self.capacity*2//5:
                    self.weights[i].append("B")
                elif self.weights[i][0] < self.capacity*2//5 and self.weights[i][0] >= self.capacity//3:
                    self.weights[i].append("C")
                elif self.weights[i][0] < self.capacity//3:
                    self.weights[i].append("D")
                    
            # def iterator():  # Wrapping the contents into an iterator
            #     for w in self.weights:
            #         yield w  # yields the current value and moves to the next one
            return (self.capacity, self.weights)