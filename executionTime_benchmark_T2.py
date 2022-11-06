from macpacking.algorithms.online import NextFit as NextFit_Online, FirstFit as FirstFit_Online, BestFit as BestFit_Online, WorstFit as WorstFit_Online
from macpacking.algorithms.offline import NextFit as NextFit_Offline, FirstFit as FirstFit_Offline, BestFit as BestFit_Offline, WorstFit as WorstFit_Offline
from macpacking.model import Online, Offline
from ExecutionTimeBenchmark import ExecutionTimeBenchMark
# from Plotter import Plotter

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt', './_datasets/jburkardt/p04_c.txt']
CANADIATES : list[Online | Offline] = [NextFit_Online(), FirstFit_Online(), BestFit_Online(), WorstFit_Online(), NextFit_Offline(), FirstFit_Offline(), BestFit_Offline(), WorstFit_Offline()]
nb_weights = [9,33,50,100,200,500]

def main():
    
    bench = ExecutionTimeBenchMark()
    ''' Outputs JSON file '''
    bench.doBenchMark(CASES, CANADIATES)
    
    ''' 
    Comment the doBenchMark function and uncomment code below as well as the Plotter import
    
    '''
    
    '''
    bench_datafile = "./executionTime_benchmark_T2.json"
    obs = bench.extract_observations(bench_datafile)
    plot = Plotter()
    plot.executionTime_graph(dic=obs, xaxis=nb_weights, filename="T2")
    '''
    
if __name__ == "__main__":
    
    main()
    
# python executionTime_benchmark_T2.py -o executionTime_benchmark_T2.json