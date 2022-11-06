import math
from .. import Solution, WeightSet
from ..model import Offline
from .online import NextFit as Nf_online, FirstFit as Ff_online, BestFit as Bf_online, WorstFit as Wf_online

class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        solution = delegation((capacity, weights))
        self.num_of_bins_created = delegation.num_of_bins_created
        self.num_of_compares = delegation.num_of_compares
        self.num_of_times_checked_bins = delegation.num_of_times_checked_bins
        return solution
    
class FirstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Ff_online()
        solution = delegation((capacity, weights))
        self.num_of_bins_created = delegation.num_of_bins_created
        self.num_of_compares = delegation.num_of_compares
        self.num_of_times_checked_bins = delegation.num_of_times_checked_bins
        return solution
    
class BestFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Bf_online()
        solution = delegation((capacity, weights))
        self.num_of_bins_created = delegation.num_of_bins_created
        self.num_of_compares = delegation.num_of_compares
        self.num_of_times_checked_bins = delegation.num_of_times_checked_bins
        return solution
    
class WorstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        solution = delegation((capacity, weights))
        self.num_of_bins_created = delegation.num_of_bins_created
        self.num_of_compares = delegation.num_of_compares
        self.num_of_times_checked_bins = delegation.num_of_times_checked_bins
        return solution

class MultiFit(Offline):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, n: int, stream: WeightSet) -> Solution:
        
        L = max(sum(stream)/n, max(stream))
        U = max((2 * sum(stream))/n, max(stream))
        X = math.inf
        
        k = len(stream)//2
        for i in range(k):
            c = (L + U)/2
            
            data = (c, stream)
            ffD = FirstFit()
            sol = ffD(data)
                    
            if len(sol) > n:
                L = c
            elif len(sol) <= n:
                U = c

        return sol
    
class LargestSum(Offline):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightSet) -> Solution:
        
        solution = [([], 0) for i in range(capacity)]
        for w in stream:
            pos = self.getSmallestWeightBin(solution)
            _bin, binWeight = solution[pos]
            _bin.append(w)
            solution[pos] = (_bin, binWeight + w)
        
        return solution
                
    def getSmallestWeightBin(self, bins):
        
        i = 0
        smallestWeight = math.inf
        for index, _bin in enumerate(bins):
            curr_bin, binWeight = _bin
            if binWeight < smallestWeight:
                smallestWeight = binWeight
                i = index
                
        return i
