from os.path import isfile, join
from os import listdir
import pyperf
from typing import TypedDict
from macpacking.model import Online, Offline
from macpacking.reader import BinppReader, JburkardtReader


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
        self.__metrics: list[str] = []

    def with_strategies(self, strats: list[Online | Offline]):
        self.__strategies.extend(strats)
        return self

    def with_cases(self, cases: list[str]):
        cases = self.list_case_files(cases)
        self.__cases.extend(cases)
        return self

    def with_metrics(self, metrics: list[str]):
        self.__metrics.extend(metrics)
        return self

    def metricBench(self, dic, metrics, algo_name,
                    algo_type, numOfWeights, binpacker):
        for metric in metrics:
            dic[metric] = dic.get(metric, {})
            dic[metric][algo_type] = dic[metric].get(algo_type, {})
            dic[metric][algo_type][algo_name] = dic[metric][algo_type].get(
                algo_name, [])
            dic[metric][algo_type][algo_name].append(
                (numOfWeights, binpacker.getMetric(metric)))

        print(f"----- {algo_name} ({algo_type}) -----")
        print()
        for metric in metrics:
            print(f'{metric} : {binpacker.getMetric(metric)}')

        return dic

    def list_case_files(self, directories: list[str]) -> list[str]:
        cases: list[str] = []
        for directory in directories:
            # get all files in directory
            if 'binpp' in directory:
                files = [
                    f'{directory}/{f}' for f in
                    listdir(directory) if isfile(join(directory, f))]
                # generate random index in the files array
                cases.append(files[0])
            elif 'jburkardt' in directory:
                cases.append(directory)

        return cases

    def finalize(self, bench_type: str = "time",
                 areWeightsSorted: bool = False):
        if bench_type == "time":
            result = []
        elif bench_type == "metric":
            result = {}
        for case in self.__cases:

            for strategy in self.__strategies:

                # get data from case
                data = None
                if "binpp" in case:
                    data = BinppReader(case)
                elif "jburkardt" in case:
                    # ./_datasets/jburkardt/p01_c.txt
                    targetFile = case.split("/")[-1].split("_")[0]
                    data = JburkardtReader(
                        [f'{targetFile}_c.txt', f'{targetFile}_w.txt'])
                else:
                    raise ValueError(f'Unkown file [{case}]')

                temp = data.offline()
                weights = temp[1]
                capacity = temp[0]
                nb_weights = len(weights)

                # check type of strategy if online of offline
                strategy_type: "Offline" | "Online" = ""
                bases = strategy.__class__.__bases__
                for base in bases:
                    strategy_type += base.__name__
                if strategy_type == "Online":
                    if strategy.__class__.__name__ == "RefinedFirstFit":
                        data = data.online(True)
                    else:
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
                else:
                    data = data.offline()

                binpacker = strategy
                binpacker(data)

                if bench_type == "time":
                    elem: SpaceElement = {
                        'name': self.__build_name(strategy, nb_weights,
                                                  capacity),
                        'strategy': strategy,
                        'weights': data[1],
                        'capacity': data[0],
                        'case_': case
                    }
                    result.append(elem)
                elif bench_type == "metric":
                    self.metricBench(
                        result, self.__metrics, strategy.__class__.__name__,
                        strategy_type, nb_weights, binpacker)

        return result

    def __build_name(self, strategy: Online | Offline,
                     nb_weights: int, capacity: int) -> str:
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
        data = (e['capacity'], e['weights'])
        binpacker = e['strategy']

        # print(data)
        runner.bench_func(e['name'], binpacker, data)
