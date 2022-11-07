from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on, WorstFit as WorstFit_on, RefinedFirstFit
from benchmarking.MetricBenchmark import MetricsBenchmark


CASES = ['./_datasets/binpp/N1C1W1', './_datasets/binpp/N2C1W1', './_datasets/binpp/N3C1W1',
         './_datasets/binpp/N4C1W1', './_datasets/jburkardt/p01_c.txt', './_datasets/jburkardt/p04_c.txt']
CANADIATES = [NextFit_on(), FirstFit_on(), BestFit_on(),
              WorstFit_on(), RefinedFirstFit()]
METRICS = ['num_of_bins_created',
           'num_of_times_checked_bins', 'num_of_compares']
nb_weights = [14, 33, 50, 100, 200, 500]


def main():

    MetricsBenchmark(CASES, CANADIATES, METRICS, nb_weights, "T4")


if __name__ == "__main__":

    main()
