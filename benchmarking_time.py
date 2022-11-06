from pyperf import BenchmarkSuite
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit as NextFit_Online, FirstFit as FirstFit_Online, BestFit as BestFit_Online, WorstFit as WorstFit_Online
from macpacking.algorithms.offline import NextFit as NextFit_Offline, FirstFit as FirstFit_Offline, BestFit as BestFit_Offline, WorstFit as WorstFit_Offline, LargestSum, MultiFit
from macpacking.algorithms.baseline import MultiwayNumberPartitioning as MNP
from macpacking.algorithms.online import RefinedFirstFit
from macpacking.model import Online, Offline
from benchmark import BenchmarkSpace, run_benchmark
from Plotter import Plotter

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt', './_datasets/jburkardt/p04_c.txt']
CANADIATES : list[Online | Offline] = [NextFit_Online(), FirstFit_Online(), BestFit_Online(), WorstFit_Online(), RefinedFirstFit(),NextFit_Offline(), FirstFit_Offline(), BestFit_Offline(), WorstFit_Offline()]
CANADIATES_T5 = [MNP(), LargestSum(), MultiFit()]
CANADIATES_T4 = [RefinedFirstFit()]

bm = BenchmarkSpace()


def initialise_bench(canadiates):
    bm.with_cases(CASES)
    bm.with_strategies(canadiates)


def extract_observations(bench_file: str):
    suite = BenchmarkSuite.load(bench_file)
    result = {}
    for bench in suite.get_benchmarks():
        context = tuple(bench.get_name().split('-'))
        observations = list(bench.get_values())
        result[context] = observations
    return result

def main():
    
    #initialise benchmark space
    initialise_bench(CANADIATES_T5)
    # run_benchmark(bm)
    bench_datafile = "./benchmarking_time.json"
    obs = extract_observations(bench_datafile)
    nb_weights = [9,33,50,100,200,500] # generalise
    # createGraph(obs, nb_weights )
    plot = Plotter()
    plot.executionTime_graph(dic=obs, xaxis=nb_weights, filename="regular")
    
if __name__ == "__main__":
    main()
    
# python executionTime_benchmark_T2.py -o executionTime_benchmark_T2.json