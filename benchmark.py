import pyperf, random
from typing import TypedDict
from macpacking.model import Online, Offline
from macpacking.reader import BinppReader, JburkardtReader, Normalized_reading

class SpaceElement(TypedDict):
    name: str
    strategy: Offline | Online
    weights: list[int]
    capacity: int
    case_: str
    
class BenchmarkSpace():
    
    def __init__(self) -> None:
        self.__strategies: list[Offline | Online] = []
        self.__cases: list[str] = []        
    
    def with_strategies(self, strats: list[Online | Offline]):
        self.__strategies.extend(strats)
        return self

    def with_cases(self, cases: list[str]):
        self.__cases.extend(cases)
        return self
    
    def finalize(self, areWeightsSorted: bool = False) -> list[SpaceElement]:
        result = []
        for case in self.__cases:
            for strategy in self.__strategies:
                
                # get data from case
                data = None
                if "binpp" in case:
                    data = BinppReader(case) 
                elif "jburkardt" in case:
                    targetFile = case.split("/")[-1].split("_")[0]  # ./_datasets/jburkardt/p01_c.txt
                    data = JburkardtReader([f'{targetFile}_c.txt',f'{targetFile}_w.txt']) 
                else:
                    raise ValueError(f'Unkown file [{case}]')

                    
                # check type of strategy if online of offline
                strategy_type : "Offline" | "Online" = ""
                bases = strategy.__class__.__bases__
                for base in bases: strategy_type += base.__name__
                
                if strategy_type == "Online": 
                    data = data.online()
                    # if weights are sorted
                    if areWeightsSorted:
                        temp = []
                        for w in data[1]:
                            temp.append(w)
                        temp.sort()
                        def iterator():  
                            for w in temp:
                                yield w  
                                
                        data = (data[0], iterator())
                        
                elif strategy_type == "Offline": data = data.offline()
                
                # deconstruct data
                weights = data[1]
                nb_weights = 0
                ## handles online and offline
                for w in weights:
                    nb_weights += 1
                    
                capacity = data[0]
                
                elem : SpaceElement = {
                    'name': self.__build_name(strategy, nb_weights, capacity),
                    'strategy': strategy,
                    'weights': weights,
                    'capacity':capacity,
                    'case_':case
                }
                result.append(elem)

        return result
    
            
    def __build_name(self, strategy: Online | Offline, nb_weights: int, capacity: int) -> str:
        type_ = ""
        for base in strategy.__class__.__bases__:
            type_ = (base.__name__)
        return f'{type_}-{strategy.__class__.__name__}-{nb_weights}-{capacity}'

def run_benchmark(space: BenchmarkSpace, areWeightsSorted: bool = False):
    runner = pyperf.Runner()
    if not areWeightsSorted:
        elements: list[SpaceElement] = space.finalize()
    else:
        elements: list[SpaceElement] = space.finalize(areWeightsSorted=True)
        
    for e in elements:
        data = (e['capacity'],e['weights'])
        binpacker = e['strategy']
        runner.bench_func(e['name'], binpacker , data)