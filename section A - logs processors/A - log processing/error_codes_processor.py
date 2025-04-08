#part A
from collections import Counter
from os import listdir

CHUNK_SIZE = 1000
file_name = "logs.txt"

def extractErrorCode(line: str) -> str:
    if "Error: " in line:
        return line.split("rror: ")[-1]

#1. split file into reasonable chunks
def findTopNErrorCodes(n: int) -> Counter:
    error_frequencies = Counter()

    with open(file_name, "r") as logs_file:

        while True:
            chunk_lines = []
            for _ in range(CHUNK_SIZE):
                line = logs_file.readline().strip()
                chunk_lines.append(line)
            
            chunk_lines = [line for line in chunk_lines if line]
            if not chunk_lines:
                break

            #2, 3. count frequency of each chunk's error codes
            error_codes = [extractErrorCode(line) for line in chunk_lines]
            error_frequencies.update(error_codes)


    #find N most frequent error codes from the merged counts
    if n > -1:
        return error_frequencies.most_common(n)
    return error_frequencies

def main():
    file_name = input("Enter logs file name to analyze:\n")
    if file_name not in listdir():
        return f"{file_name} couldn't be found in this directory."
    
    n = int(input("Enter the number of most common errors you wish to be displayed (-1 for all):\n"))
    
    top_errors = findTopNErrorCodes(n)
    top_errors = sorted(top_errors, key=lambda pair: pair[1], reverse=True)

    for error_name, error_count in top_errors:
        print(f"{error_name}: {error_count}")

main()

#time and space complexities calculations
'''
Suppose:    L is the total number of lines in the input file.
            K is the chunk size
            E is the distinct error codes
            (E <= L)
    Time Complexity: O(L + Elog(E))
We have to go over the entire file, so it's theta(L) to read, no matter how we divide it by chunks.
The time it takes to sort the error logs (in order to retrieve the top N ones)
depends on the distict number of error logs, which will take O(ElogE) with common, optimised sorting algorithms.
    
    Space Complexity: O(E)
The storage of Counter & chunk_lines.
Each chunk is of constant K lines, and doesnt scale with the input.
Counter needs storage relative to the number of distinct error logs that it keeps as keys, O(E)
'''