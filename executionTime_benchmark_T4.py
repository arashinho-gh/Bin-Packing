from macpacking.algorithms.online import NextFit, FirstFit, BestFit,\
    WorstFit, RefinedFirstFit
from macpacking.model import Online, Offline
from benchmarking.ExecutionTimeBenchmark import ExecutionTimeBenchMark
# from benchmarking.Plotter import Plotter

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1',
         './_datasets/binpp/N3C1W1',
         './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt',
         './_datasets/jburkardt/p04_c.txt']
CANADIATES: list[Online | Offline] = [
    NextFit(), FirstFit(), BestFit(), WorstFit(), RefinedFirstFit()]
nb_weights = [9, 33, 50, 100, 200, 500]


def main():

    bench = ExecutionTimeBenchMark()
    ''' Outputs JSON file '''
    bench.doBenchMark(CASES, CANADIATES)

    '''
    Comment the doBenchMark function and uncomment code below as
    well as the Plotter import
    '''

    '''
    bench_datafile = "./executionTime_benchmark_T4.json"
    obs = bench.extract_observations(bench_datafile)
    plot = Plotter()
    plot.executionTime_graph(dic=obs, xaxis=nb_weights, filename="T4")
    '''


if __name__ == "__main__":

    main()

# python executionTime_benchmark_T4.py -o executionTime_benchmark_T4.json
