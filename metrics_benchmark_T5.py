from macpacking.algorithms.offline import FirstFit, LargestSum, MultiFit
from benchmarking.MetricBenchmark import MetricsBenchmark

CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1',
         './_datasets/binpp/N3C1W1',
         './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt',
         './_datasets/jburkardt/p04_c.txt']
CANADIATES = [FirstFit(), LargestSum(), MultiFit()]
METRICS = ['num_of_bins_created',
           'num_of_times_checked_bins', 'num_of_compares']
nb_weights = [14, 33, 50, 100, 200, 500]


def main():

    MetricsBenchmark(CASES, CANADIATES, METRICS, nb_weights, "T5")


if __name__ == "__main__":

    main()
