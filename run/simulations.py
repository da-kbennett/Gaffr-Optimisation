import pandas as pd
import os
import glob
import time
from concurrent.futures import ProcessPoolExecutor
import argparse
import copy
from solve_regular import solve_regular

def solve_job(job):
    return solve_regular(runtime_options=job['runtime_options'])

def run_sensitivity(runtime_options=None, options=None):
    
    if options is None or 'count' not in options:
        runs = int(input("How many simulations would you like to run? "))
        processes = int(input("How many processes you want to run in parallel? "))
    else:
        runs = options.get('count', 1)
        processes = options.get('processes', 1)

    start = time.time()

    all_jobs = [{'run_no': str(i+1), 'randomized': True, 'runtime_options': copy.deepcopy(runtime_options)} for i in range(runs)]

    # Use the solve_job function instead of lambda in the map method
    with ProcessPoolExecutor(max_workers=processes) as executor:
        results = list(executor.map(solve_job, all_jobs))

    end = time.time()

    print()
    print(f"Total time taken is {(end - start) / 60:.2f} minutes")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Run sensitivity analysis")
        parser.add_argument("--no", type=int, help="Number of runs")
        parser.add_argument("--parallel", type=int, help="Number of parallel runs")
        args = parser.parse_args()
        options = {}
        if args.no:
            options['count'] = args.no
        if args.parallel:
            options['processes'] = args.parallel
    except:
        options = None

    run_sensitivity(options)