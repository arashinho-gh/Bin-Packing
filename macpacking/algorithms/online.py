import math
from .. import Solution, WeightStream, NomralizedWeightSet
from ..model import Online

class NextFit(Online):
    
    def __init__(self) -> None:
        super().__init__()
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
        
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
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
        
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
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
        
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
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
        
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
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
        
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [([],0)]
        index = 0
        for w in stream:
            self.num_of_bins_created += 1
            solution[index] = ([w], w)
            index += 1


class RefinedFirstFit(Online):

    def __init__(self) -> None:
        super().__init__()
        self.A=[]
        self.B=[]
        self.C=[]
        self.D=[]
        self.num_of_bins_created = 0
        self.num_of_compares = 0
        self.num_of_times_checked_bins = 0
    
    def compare(self,capacity, i):
        fit = 0
        """ check if the value will fit in the A class"""
        if len(self.A) > 1 and fit==0:
            for k in self.A:
                self.num_of_compares += 1
                self.num_of_times_checked_bins +=1
                if sum(k) + i[0] <= capacity:
                    k.append(i[0])
                    fit += 1
                    break
        """ check if the value will fit in the B class"""
        if len(self.B) > 1 and fit==0:
            for k in self.B:
                self.num_of_compares += 1
                self.num_of_times_checked_bins +=1
                if sum(k) + i[0] <= capacity:
                    k.append(i[0])
                    fit += 1
                    break
        """ check if the value will fit in the C class"""
        if len(self.C) > 1 and fit==0:
            for k in self.C:
                self.num_of_compares += 1
                self.num_of_times_checked_bins +=1
                if sum(k) + i[0] <= capacity:
                    k.append(i[0])
                    fit += 1
                    break
        """ check if the value will fit in the D class"""
        if len(self.D) > 1 and fit==0:
            for k in self.D:
                self.num_of_compares += 1
                self.num_of_times_checked_bins +=1
                if sum(k) + i[0] <= capacity:
                    k.append(i[0])
                    fit += 1
                    break
        return fit
        
    def _process(self, capacity: int, stream: NomralizedWeightSet) -> Solution:
        
        solution = [([],0)]
        # print(stream)
        for i in stream:
            ''' compare the weight to each heurestic and place it its corresponding class'''
            if i[1] == "A":
                fit = self.compare(capacity, i)
                if fit == 0:
                    self.A.append([i[0]])
                    self.num_of_bins_created += 1
            elif i[1] == "B":
                fit = self.compare(capacity, i)
                if fit == 0:
                    self.B.append([i[0]])
                    self.num_of_bins_created += 1
            elif i[1] == "C":
                fit = self.compare(capacity, i)
                if fit == 0:
                    self.D.append([i[0]])
                    self.num_of_bins_created += 1
            elif i[1] == "D":
                fit = self.compare(capacity, i)
                if fit == 0:
                    self.D.append([i[0]])
                    self.num_of_bins_created += 1
                    
        data=self.A+self.B+self.C+self.D
        for k in range(len(data)-1):
            solution.append((data[k], sum(data[k])))
        return(solution)