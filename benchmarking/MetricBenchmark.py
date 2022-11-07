from benchmarking.Plotter import Plotter
from benchmarking.benchmark import BenchmarkSpace


class MetricsBenchmark():

    def __init__(self, CASES, CANADIATES, METRICS, nb_weights,
                 filename, artWeightsSorted=False) -> None:
        bm = BenchmarkSpace()
        ''' Load Benchmark Data'''
        bm.with_cases(CASES)
        bm.with_strategies(CANADIATES)
        bm.with_metrics(METRICS)
        ''' Finalize Benchmark'''
        data = bm.finalize(bench_type="metric",
                           areWeightsSorted=artWeightsSorted)
        ''' Plot Data '''
        plotter = Plotter()
        plotter.metric_graph(data, nb_weights, filename)
