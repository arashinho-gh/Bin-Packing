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
