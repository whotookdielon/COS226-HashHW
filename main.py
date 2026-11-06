'''
# Name: Dylan Fish
# Course: COS 226
# Date: 11/6/2026
This program reads movie records from a CSV file.
It builds one hash table with movie titles as keys and another with quotes as keys.
Collisions are counted whenever an occupied node or slot is examined during insertion.
Wasted space means buckets or slots left empty.
Duplicate titles and quotes are kept; no movie records are overwritten.
'''

import csv
import sys
import time

TABLE_SIZE = 20011


def hash_key(key):
    # A poor hash: keys starting with the same character get the same index.
    if key == "":
        return 0
    return ord(key[0])


class HashTable:
    # Creates an array-based table that uses linear probing for collisions.
    def __init__(self):
        self.slots = [None] * TABLE_SIZE
        self.collisions = 0
        self.count = 0

    # Adds a movie, trying the next slot whenever one is already occupied.
    def insert(self, key, movie):
        index = hash_key(key) % TABLE_SIZE
        for attempt in range(TABLE_SIZE):
            if self.slots[index] is None:
                self.slots[index] = (key, movie)
                self.count += 1
                return
            self.collisions += 1
            index = (index + 1) % TABLE_SIZE
        raise RuntimeError("The hash table is full")

    # Finds all records with a matching key, including duplicates.
    def find_all(self, key):
        matches = []
        index = hash_key(key) % TABLE_SIZE
        for attempt in range(TABLE_SIZE):
            item = self.slots[index]
            if item is None:
                break
            if item[0] == key:
                matches.append(item[1])
            index = (index + 1) % TABLE_SIZE
        return matches

    # Counts empty slots in the table.
    def wasted_space(self):
        return TABLE_SIZE - self.count


def load_movies(filename):
    # Opens the movie CSV file and loads its rows into a list.
    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "movie_title" not in reader.fieldnames or "quote" not in reader.fieldnames:
            raise ValueError("CSV needs movie_title and quote columns")
        movies = []
        for row in reader:
            if row.get("movie_title") is not None and row.get("quote") is not None:
                movies.append(row)
    return movies


def show_table(movies, key_name, label):
    # Builds one hash table, times the insertions, and prints the results.
    table = HashTable()
    start = time.perf_counter()
    for movie in movies:
        table.insert(movie[key_name], movie)
    seconds = time.perf_counter() - start

    # Check that lookup returns all records sharing the first movie's key.
    correct = table.count == len(movies)
    if movies:
        sample = movies[0][key_name]
        expected = sum(1 for movie in movies if movie[key_name] == sample)
        correct = correct and len(table.find_all(sample)) == expected

    print("\n" + label + " HASH TABLE")
    print("  Records inserted:", table.count)
    print("  Total buckets/slots:", TABLE_SIZE)
    print("  Wasted space:", table.wasted_space())
    print("  Collisions:", table.collisions)
    print(f"  Construction time: {seconds:.6f} seconds")
    print("  Lookup check:", "PASS" if correct else "FAIL")
    if not correct:
        raise AssertionError("Some movies could not be found")


def main():
    # Reads the optional CSV filename and runs both hash table tests.
    filename = sys.argv[1] if len(sys.argv) > 1 else "MOCK_DATA.csv"
    movies = load_movies(filename)
    print("ATTEMPT 3: Linear probing with first-letter hash")
    print("CSV records loaded:", len(movies))
    print("Collision = occupied node/slot inspected during insertion")
    show_table(movies, "movie_title", "TITLE")
    show_table(movies, "quote", "QUOTE")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print("Error:", error)
        sys.exit(1)