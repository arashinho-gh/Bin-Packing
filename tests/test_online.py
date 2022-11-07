from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.algorithms.online import NextFit, FirstFit, BestFit, WorstFit, RefinedFirstFit

algos = [NextFit(), FirstFit(), BestFit(), WorstFit(), RefinedFirstFit()]

''' Test if algorithms output optimal solution on a easy dataset'''


def test_optimalSolution():
    dataset = ['p01_c.txt',
               'p01_w.txt', 'p01_s.txt']

    data = JburkardtReader(dataset)
    d = data.offline()
    solution = len(set(data.data['solution']))

    for algo in algos:
        if algo.__class__.__name__ == "RefinedFirstFit":
            d = data.online(True)
        else:
            d = data.online()
        binpacker = algo
        sol = binpacker(d)
        assert solution == len(sol)


''' Check if algorithms do not output optimal solution on a hard dataset '''


def test_NOToptimalSolution():
    dataset = ['./_datasets/binpp-hard/HARD0.BPP.txt']

    data = BinppReader(dataset[0])

    solution = 56

    for algo in algos:
        if algo.__class__.__name__ == "RefinedFirstFit":
            d = data.online(True)
        else:
            d = data.online()
        binpacker = algo
        sol = binpacker(d)
        assert solution != len(sol)
