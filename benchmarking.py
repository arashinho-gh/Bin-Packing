from os import listdir
from os.path import isfile, join, basename
from random import shuffle
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on,WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of,BestFit as BestFit_of,WorstFit as WorstFit_of

from macpacking.reader import BinppReader
import matplotlib.pyplot as plt

# CASES = './_datasets/binpp/N4C2W2'

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1', './_datasets/binpp/N4C1W1']

def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)
    run_bench(cases, True)

def list_case_files(dir: any) -> list[str]:
    lst = []
    for case in dir:
        t = [f'{case}/{f}' for f in listdir(case) if isfile(join(case, f))]
        shuffle(t)
        lst.append(t[0])
        lst.append(t[1])
    return lst

def sortStream(data, new_cap = 0): # take offline input
    stream = sorted(data[1], reverse = True)
    if new_cap:
        cap = new_cap
    else: 
        cap = data[0]
        
    cap = data[0]
    def iterator():  
        for w in stream:
            yield w  
    return (cap, iterator())

def updateCap(data, val):
    data[0] = val
    return data
    
algos = [NextFit_on(), FirstFit_on(), BestFit_on(), WorstFit_on(), NextFit_of(), FirstFit_of(), BestFit_of(), WorstFit_of()]

def run_bench(cases: list[str], sorted = False):
    dic = {
        'Online': {},
        'Offline': {}
    }
    for case_index, case in enumerate(cases):
        print(f"----------------------- Case({case_index}) -----------------------")
        print()

        for index, algo in enumerate(algos):
            data = BinppReader(case)
            temp = BinppReader(case).offline()
            cap = temp[0]
            weights = temp[1]
            numOfWeights = len(weights)
            
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
            
            dic[algo_type][numOfWeights] = dic[algo_type].get(numOfWeights, {})
            dic[algo_type][numOfWeights][algo_name] = dic[algo_type][numOfWeights].get(algo_name, {})
            dic[algo_type][numOfWeights][algo_name]['bins-created'] = binpacker.num_of_bins_created
            dic[algo_type][numOfWeights][algo_name]['bins-checked'] = binpacker.num_of_times_checked_bins
            dic[algo_type][numOfWeights][algo_name]['compares'] = binpacker.num_of_compares

            '''
            print(f"----- {algo_name} ({algo_type}) -----")
            print()
            print(f"bins: {len(solution)}")
            print("Number of bins created: ", binpacker.num_of_bins_created)
            print("Number of times weight is checked with previous bins: ", binpacker.num_of_times_checked_bins)
            print("Number of compares: ", binpacker.num_of_compares)
            '''
    
    print(dic['Offline'].keys())
    plt.plot(list(dic['Offline'].keys()))
    plt.ylabel('some numbers')
    plt.show()    

if __name__ == "__main__":
    
    main()
