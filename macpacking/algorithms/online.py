import math, heapq
from msilib.schema import Class
from .. import Solution, WeightStream
from ..model import Online

class NextFit(Online):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            self.num_of_compares += 1
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                self.num_of_bins_created += 1
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
                
        return solution

class FirstFit(Online):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:

        solution = [([],0)]
        for w in stream:
            for i in range(len(solution) + 1):
                ''' if weight doesn't fit in any previous bin add a new bin '''
                if i == len(solution):
                    self.num_of_bins_created += 1
                    solution.append(([w], w))
                    break
                ''' check if weight fits in a previous bin and add it '''
                _bin, bin_cap = solution[i]
                self.num_of_times_checked_bins += 1
                self.num_of_compares += 1
                if bin_cap + w <= capacity:
                    _bin.append(w)
                    solution[i] = (_bin,bin_cap + w)
                    break
        return solution

class BestFit(Online):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [([],0)]
        for w in stream:
            space_left = math.inf
            index = -math.inf
            ''' find bin where the weight will result in the tightest fit '''
            for i in range(len(solution)):
                self.num_of_times_checked_bins += 1
                _bin, bin_cap = solution[i]
                self.num_of_compares += 1
                if bin_cap + w <= capacity and capacity - (bin_cap + w) < space_left:
                    space_left = capacity - (bin_cap + w)
                    index = i
            ''' if a bin of the tightest bin exists then added otherwise create a new bin '''
            if index >= 0:
                _bin, bin_cap = solution[index]
                _bin.append(w)
                solution[index] = (_bin, bin_cap + w)
            else:
                self.num_of_bins_created += 1
                solution.append(([w], w))
            
        return solution
       
class WorstFit(Online):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [([],0)]
        for w in stream:
            space_left = -math.inf
            index = -math.inf
            ''' find bin where the weight will result in the tightest fit '''
            for i in range(len(solution)):
                self.num_of_times_checked_bins += 1
                _bin, bin_cap = solution[i]
                self.num_of_compares += 1
                if bin_cap + w <= capacity and capacity - (bin_cap + w) > space_left:
                    space_left = capacity - (bin_cap + w)
                    index = i
            ''' if a bin of the tightest bin exists then added otherwise create a new bin '''
            if index >= 0:
                _bin, bin_cap = solution[index]
                _bin.append(w)
                solution[index] = (_bin, bin_cap + w)
            else:
                self.num_of_bins_created += 1
                solution.append(([w], w))
            
        return solution  
    
class WorstCase(Online):
    
    def __init__(self) -> None:
        super().__init__()
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [([],0)]
        index = 0
        for w in stream:
            self.num_of_bins_created += 1
            solution[index] = ([w], w)
            index += 1

