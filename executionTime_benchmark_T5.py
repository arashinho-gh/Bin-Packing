from macpacking.algorithms.offline import FirstFit, LargestSum, MultiFit
from macpacking.model import Online, Offline
from ExecutionTimeBenchmark import ExecutionTimeBenchMark
# from Plotter import Plotter

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt', './_datasets/jburkardt/p04_c.txt']
CANADIATES : Online | Offline  = [FirstFit(), LargestSum(), MultiFit()]
nb_weights = [14,33,50,100,200,500]


def main():
    
    bench = ExecutionTimeBenchMark()
    ''' Outputs JSON file '''
    bench.doBenchMark(CASES, CANADIATES)
    
    ''' 
    Comment the doBenchMark function and uncomment code below as well as the Plotter import
    
    '''
    
    '''
    bench_datafile = "./executionTime_benchmark_T5.json"
    obs = bench.extract_observations(bench_datafile)
    plot = Plotter()
    plot.executionTime_graph(dic=obs, xaxis=nb_weights, filename="T5")
    '''
    
if __name__ == "__main__":
    
    main()
    
# python executionTime_benchmark_T5.py -o executionTime_benchmark_T5.json