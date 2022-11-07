from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.algorithms.offline import NextFit, FirstFit, BestFit, WorstFit

algos = [NextFit(), FirstFit(), WorstFit(), BestFit()]
''' Test if algorithms output optimal solution on a easy dataset'''


def test_optimalSolution():
    dataset = ['p01_c.txt',
               'p01_w.txt', 'p01_s.txt']

    data = JburkardtReader(dataset)
    d = data.offline()
    solution = len(set(data.data['solution']))

    for algo in algos:
        binpacker = algo
        sol = binpacker(d)
        assert solution == len(sol)


''' Check if algorithms do not output optimal solution on a hard dataset '''


def test_NOToptimalSolution():
    dataset = ['./_datasets/binpp-hard/HARD0.BPP.txt']

    data = BinppReader(dataset[0])
    d = data.offline()

    solution = 56

    for algo in algos:
        binpacker = algo
        sol = binpacker(d)
        assert solution != len(sol)
