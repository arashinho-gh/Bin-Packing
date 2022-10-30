import pyperf
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit
from macpacking.reader import BinppReader
from macpacking.reader import JburkardtReader
from tests.test_reader import test_binpp_reader
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on,WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of,BestFit as BestFit_of,WorstFit as WorstFit_of

# We consider:
#   - 500 objects (N4)
#   - bin capacity of 120 (C2)
#   - and weight in the [20,100] interval (W2)
CASES = './_datasets/binpp-hard'

algos = [NextFit_on(), FirstFit_on(), BestFit_on(), WorstFit_on(), NextFit_of(), FirstFit_of(), BestFit_of(), WorstFit_of()]

def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)
    run_bench(cases)


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench(cases: list[str]):
    runner = pyperf.Runner()
    for case_index, case in enumerate(cases):
        print(f"===== Case {case_index} ======")
        for index, algo in enumerate(algos):
            
            data = BinppReader(case)
            algo_type = None
            algo_name = algo.__class__.__name__
            binpacker = algo
            
            if index < 4: # online
                algo_type = 'Online' 
                data = data.online()
                
            else: # offline
                algo_type = 'Offline' 
                data = data.offline()
                
            solution = binpacker.__call__(data)
            print(f"{algo_name} - ({algo_type}) : {len(solution)}")

if __name__ == "__main__":
    main()
