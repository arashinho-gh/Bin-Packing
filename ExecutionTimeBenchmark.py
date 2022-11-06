from pyperf import BenchmarkSuite
from benchmark import BenchmarkSpace, run_benchmark

class ExecutionTimeBenchMark():
    
    def doBenchMark(self, CASES, CANADIATES):
        bm = BenchmarkSpace()
        bm.with_cases(CASES)
        bm.with_strategies(CANADIATES)
        run_benchmark(bm)
    
    def extract_observations(self, bench_file: str):
        suite = BenchmarkSuite.load(bench_file)
        result = {}
        for bench in suite.get_benchmarks():
            context = tuple(bench.get_name().split('-'))
            observations = list(bench.get_values())
            result[context] = observations
        return result

