from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit as NextFit_on, FirstFit as FirstFit_on, BestFit as BestFit_on,WorstFit as WorstFit_on
from macpacking.algorithms.offline import NextFit as NextFit_of, FirstFit as FirstFit_of,BestFit as BestFit_of,WorstFit as WorstFit_of

from macpacking.reader import BinppReader

CASES = './_datasets/binpp/N4C2W2'


def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)
    run_bench(cases)

def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench(cases: list[str]):
    
    index = 0
    
    for case in cases:
        data_nf_on = BinppReader(case).online()
        data_ff_on = BinppReader(case).online()
        data_bf_on = BinppReader(case).online()
        data_wf_on = BinppReader(case).online()

        data_nf_of = BinppReader(case).offline()
        data_ff_of = BinppReader(case).offline()
        data_bf_of = BinppReader(case).offline()
        data_wf_of = BinppReader(case).offline()
        
        binpacker_nf_on = NextFit_on()
        binpacker_ff_on = FirstFit_on()
        binpacker_bf_on = BestFit_on()
        binpacker_wf_on = WorstFit_on()
        
        binpacker_nf_of = NextFit_of()
        binpacker_ff_of = FirstFit_of()
        binpacker_bf_of = BestFit_of()
        binpacker_wf_of = WorstFit_of()
        
        binpacker_nf_on.__call__(data_nf_on)
        binpacker_ff_on.__call__(data_ff_on)
        binpacker_bf_on.__call__(data_bf_on)
        binpacker_wf_on.__call__(data_wf_on)
        
        binpacker_nf_of.__call__(data_nf_of)
        binpacker_ff_of.__call__(data_ff_of)
        binpacker_bf_of.__call__(data_bf_of)
        binpacker_wf_of.__call__(data_wf_of)
        
        print(f"----------------------- Case({index}) -----------------------")
        print()
        print("----------- NextFit -----------")
        print()
        print("----- Online -----")
        print("Number of bins created: ", binpacker_nf_on.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_nf_on.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_nf_on.num_of_compares)

        print(f"----------- FirstFit -----------")
        print("Number of bins created: ", binpacker_ff_on.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_ff_on.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_ff_on.num_of_compares)

        print(f"----------- BestFit -----------")
        print("Number of bins created: ", binpacker_bf_on.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_bf_on.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_bf_on.num_of_compares)

        print(f"----------- WorstFit -----------")
        print("Number of bins created: ", binpacker_wf_on.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_wf_on.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_wf_on.num_of_compares)
        print()
        print("----- Offline -----")
        print()
        print(f"----------- NextFit -----------")
        print("Number of bins created: ", binpacker_nf_of.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_nf_of.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_nf_of.num_of_compares)

        print(f"----------- FirstFit -----------")
        print("Number of bins created: ", binpacker_ff_of.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_ff_of.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_ff_of.num_of_compares)

        print(f"----------- BestFit -----------")
        print("Number of bins created: ", binpacker_bf_of.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_bf_of.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_bf_of.num_of_compares)

        print(f"----------- WorstFit -----------")
        print("Number of bins created: ", binpacker_wf_of.num_of_bins_created)
        print("Number of times weight is checked with previous bins: ", binpacker_wf_of.num_of_times_checked_bins)
        print("Number of compares: ", binpacker_wf_of.num_of_compares)
    
        index += 1
        break
if __name__ == "__main__":
    main()
