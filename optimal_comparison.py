from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit
from macpacking.reader import BinppReader
from macpacking.reader import JburkardtReader
from tests.test_reader import test_binpp_reader
import matplotlib.pyplot as plt
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on, WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of, BestFit as BestFit_of, WorstFit as WorstFit_of
from macpacking.algorithms.baseline import BenMaier as baseline_of


# uncomment each area for the corresponding dataset you want to choose

# We consider:
#   - 500 objects (N4)
#   - bin capacity of 120 (C2)
#   - and weight in the [20,100] interval (W2)
# We will consider the continuous margin of improvement for of each algorithm within each case
file = "_datasets/optimal_values/binpp.csv"
format = "N4C2W2"
CASES = './_datasets/binpp/N4C2W2'


# We consider:
#   The jburkardt dataset
# We will consider the continuous margin of improvement for of each algorithm within each case
"""file = "_datasets/optimal_values/jburkardt.csv"
format="p_"
CASES = './_datasets/jburkardt'"""


def main(file, format, CASES):
    algos = [NextFit_on(), FirstFit_on(), BestFit_on(), WorstFit_on(
    ), NextFit_of(), FirstFit_of(), BestFit_of(), WorstFit_of(), baseline_of()]
    optimal_solutions = optimalSolutions(file, format)
    cases = list_case_files(CASES)

    """In case we want to iterate through the jburkardt file"""
    if "jburkardt" in cases:
        cases_jpurkardt = []
        for i in range(4):
            cases_jpurkardt.append(cases[i*3:i*3+3])
        cases = cases_jpurkardt

    run_bench(cases, algos, optimal_solutions)


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench(cases: list[str], algos, optimal_solutions):
    dataset = []
    for case_index, case in enumerate(cases):
        #print(f"===== Case {case_index} ======")
        optimal = int(optimal_solutions[case_index][1])
        dataset.append([case_index])
       #print(f"optimal solution : {optimal}")
        for index, algo in enumerate(algos):

            data = BinppReader(case)
            algo_type = None
            algo_name = algo.__class__.__name__
            binpacker = algo

            if index < 4:  # online
                algo_type = 'Online'
                data = data.online()

            else:  # offline
                algo_type = 'Offline'
                data = data.offline()

            solution = binpacker.__call__(data)
            #print(f"{algo_name} - ({algo_type}) : {len(solution)} - {len(solution) - optimal}")
            dataset[case_index].append(len(solution)-optimal)
    for i in dataset:
        x = [i[0], i[0], i[0], i[0], i[0], i[0], i[0], i[0], i[0]]
        y = [i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
        colors = ["red", "green", "blue", "yellow",
                  "pink", "black", "orange", "purple", "gray"]
        plt.scatter(x, y, c=colors)
    plt.ylabel("Continuous difference")
    plt.xlabel("Cases")
    plt.show()


def optimalSolutions(file, format):
    '''finds the optimal values from the oracle csv files'''
    optimal_solutions = []
    with open(file, mode='r') as input:
        final = len([*format])
        while True:
            data = input.readline().strip().split()
            if data == []:
                break
            if data[0][0:final] == format:
                optimal_solutions.append(data)
    return optimal_solutions


if __name__ == "__main__":
    main(file, format, CASES)
