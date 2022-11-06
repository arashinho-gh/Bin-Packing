import pyperf
from os import listdir
from random import shuffle
from os.path import isfile, join, basename
from macpacking.reader import BinppReader
from macpacking.reader import JburkardtReader
from tests.test_reader import test_binpp_reader
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on,WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of,BestFit as BestFit_of,WorstFit as WorstFit_of
from macpacking.algorithms.online import RefinedFirstFit

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C2W2']

"""testing if the RefindFirstFit algorithm and the Normalize_reading works"""

def main(CASES):
    '''Example of benchmark code'''
    cases = list_case_files(CASES)
    index = 0
    for case in cases:
        print(f"----------------------- Case({index}) -----------------------")
        data = BinppReader(case).online(True)
        binpacker = RefinedFirstFit()
        solution = binpacker.__call__(data)
        print(len(solution))
        print("Number of bins created: ", binpacker.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker.num_of_times_checked_bins)
        print("Number of compares: ", binpacker.num_of_compares)
        index +=1

def list_case_files(dir: str) -> list[str]:
    lst = []
    for case in dir:
        t = [f'{case}/{f}' for f in listdir(case) if isfile(join(case, f))]
        shuffle(t)
        lst.append(t[0])
        # lst.append(t[1])
    return lst

if __name__=="__main__":
    main(CASES)