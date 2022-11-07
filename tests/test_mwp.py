from macpacking.algorithms.offline import LargestSum, MultiFit

algos = [LargestSum(), MultiFit()]
''' Test if algorithms output optimal solution on a easy dataset'''

''' data set '''
weights = [1, 2, 3, 1, 1, 1]
cap = 3
solution = sorted([3, 3, 3])


def test_optimalSolution():
    data = (cap, weights)

    for algo in algos:
        binpacker = algo
        sol = binpacker(data)
        ''' place the sum of each bin in an array and sort it to compare with optimal solution '''
        bin_sums = []
        for _bin in sol:
            bin_sums.append(_bin[1])
        bin_sums.sort()
        assert bin_sums == solution
        assert len(sol) == cap
