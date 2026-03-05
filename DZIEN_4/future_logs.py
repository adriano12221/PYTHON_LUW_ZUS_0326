from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


def analyze_log(file_name):

    print(f"Start analyzing {file_name}")

    time.sleep(random.uniform(1,3))  # symulacja czytania pliku

    errors = random.randint(0,50)

    print(f"Finished {file_name} -> errors: {errors}")

    return file_name, errors


log_files = [
    "server1.log",
    "server2.log",
    "server3.log",
    "server4.log",
    "server5.log"
]


results = []

with ThreadPoolExecutor(max_workers=3) as executor:

    futures = [executor.submit(analyze_log, file) for file in log_files]

    for future in as_completed(futures):

        file_name, errors = future.result()
        results.append((file_name, errors))


print("\nSummary:")

for file, errors in results:
    print(f"{file} -> {errors} errors")
