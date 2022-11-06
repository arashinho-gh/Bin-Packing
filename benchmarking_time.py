from pyperf import BenchmarkSuite
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit as NextFit_Online, FirstFit as FirstFit_Online, BestFit as BestFit_Online, WorstFit as WorstFit_Online
from macpacking.algorithms.offline import NextFit as NextFit_Offline, FirstFit as FirstFit_Offline, BestFit as BestFit_Offline, WorstFit as WorstFit_Offline, LargestSum, MultiFit
from macpacking.algorithms.baseline import MultiwayNumberPartitioning as MNP
from macpacking.model import Online, Offline
from benchmark import BenchmarkSpace, run_benchmark
from matplotlib import pyplot as plt
from statistics import mean
from itertools import product

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt', './_datasets/jburkardt/p04_c.txt']
CANADIATES : list[Online | Offline] = [NextFit_Online(), FirstFit_Online(), BestFit_Online(), WorstFit_Online(), NextFit_Offline(), FirstFit_Offline(), BestFit_Offline(), WorstFit_Offline()]
CANADIATES_T5 = [MNP(), LargestSum(), MultiFit()]

bm = BenchmarkSpace()

Context = tuple[str, str, str, str]
Observations = dict[Context, list[float]]  ## Bind Contexts to Observations

def list_case_files(directories: list[str]) -> list[str]:
    cases: list[str] = []
    for directory in directories:
        # get all files in directory
        if 'binpp' in directory:
            files = [f'{directory}/{f}' for f in listdir(directory) if isfile(join(directory, f))]
            # generate random index in the files array
            cases.append(files[0])
        elif 'jburkardt' in directory:
            cases.append(directory)
            
    return cases

def initialise_bench(canadiates):
    cases = list_case_files(CASES)
    bm.with_cases(cases)
    bm.with_strategies(canadiates)


def extract_observations(bench_file: str) -> Observations:
    suite = BenchmarkSuite.load(bench_file)
    result = {}
    for bench in suite.get_benchmarks():
        context = tuple(bench.get_name().split('-'))
        observations = list(bench.get_values())
        result[context] = observations
    return result

##### GRRAHPING #######

def prettyfy_plot(fig, axes, w: int, h: int):
    for ax in axes.flat:
        ax.label_outer()
    fig.set_size_inches(w, h)
    fig.tight_layout()

def calcAvg(obs):
    for key, val in obs.items():
        obs[key] = (sum(val) / len(val)) * 1000
    return obs


def plot_reg_online_offline(obs: Observations,nb_Weights:list[int], ax, ax2):
    observed = calcAvg(obs)
    
    data = {}
    
    for key, val in (observed.items()):
        _type = key[0]
        algo_name = key[1]
        numWeights = key[2]
        cap = key[3]
        
        data[_type] = data.get(_type, {})
        data[_type][algo_name] = data[_type].get(algo_name, [])
        data[_type][algo_name].append((int(numWeights), val))

    # sort data
    for key, val in data.items():
        for algo in data[key]:
            temp = data[key][algo]
            temp.sort(key=lambda x:x[0])
            for i in range(len(temp)):
                temp[i] = temp[i][1]
            data[key][algo] = temp
    # plot
    for key in data.keys():
        print(data)
        if key == "Online" : 
            canvas = ax
        elif key == "Offline": 
            canvas = ax2
        
        canvas.set_title(f'{key} - BinPacking')

        for algo in data[key]:
            # print(data[key][algo][1])
            canvas.plot(nb_Weights, data[key][algo], label = algo + "-" + key, linestyle='--', marker='o')    
        canvas.legend()
        canvas.set(xlabel='|weights|', ylabel='avg time(ms)')

def createGraph(obs:Observations, nb_weights:list[int]):
    f = plt.figure(figsize=(20, 10))
    online_graph = f.add_subplot(121)
    offline_graph = f.add_subplot(122)
    plot_reg_online_offline(obs,nb_weights, online_graph, offline_graph)
    f.savefig('./execution_benchmark_T5.pdf') 

def main():
    
    #initialise benchmark space
    initialise_bench(CANADIATES_T5)
    # run_benchmark(bm)
    
    bench_datafile = "./benchmarking_time_T5.json"
    obs = extract_observations(bench_datafile)
    nb_weights = [9,33,50,100,200,500] # generalise
    createGraph(obs, nb_weights )

if __name__ == "__main__":
    main()
    
# python benchmarking_time.py -o benchmarking_time.json