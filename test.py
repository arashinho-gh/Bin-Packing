import pyperf
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit
from macpacking.reader import BinppReader
from macpacking.reader import JburkardtReader
from tests.test_reader import test_binpp_reader
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on,WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of,BestFit as BestFit_of,WorstFit as WorstFit_of, MultiFit as MF, LargestSum as mnp
from macpacking.algorithms.baseline import MultiwayNumberPartitioning as m
import binpacking as bp

CASES = './_datasets/binpp/N4C2W2'


def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)[:1]
    print(cases)
    run_bench(cases) 


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench(cases: list[str]):
    for case in cases:
        name = basename(case)
        data = BinppReader(case).offline()
        binpacker = MF()
        # data = (5, data[1])
        sol = binpacker(data)
        arr = []
        for i in sol:
            arr.append(i[1])
        print(set(arr), len(arr))
        print("-----------")
        binpacker = mnp()
        sol3 = binpacker(data)
        arr = []
        for i in sol3:
            arr.append(i[1])
        print(set(arr), len(arr))
        print("-----------")

        sol2 = m()
        print(data[0])
        t = (sol2._process(data[0],data[1]))
        ans = []
        for i in t:
            ans.append(sum(i))
        print(set(ans), len(ans))
if __name__ == "__main__":
    main()
