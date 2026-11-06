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

TABLE_SIZE = 4099


def hash_key(key):
    # A poor hash: keys starting with the same character get the same index.
    if key == "":
        return 0
    return ord(key[0])


class Node:
    # Stores one movie and the next node in its linked list.
    def __init__(self, key, movie, next_node=None):
        self.key = key
        self.movie = movie
        self.next = next_node


class HashTable:
    # Creates a hash table that stores collisions in linked lists.
    def __init__(self):
        self.buckets = [None] * TABLE_SIZE
        self.collisions = 0
        self.count = 0

    # Adds a movie and counts every occupied node it passes in that bucket.
    def insert(self, key, movie):
        index = hash_key(key) % TABLE_SIZE
        current = self.buckets[index]
        while current is not None:
            self.collisions += 1
            current = current.next
        self.buckets[index] = Node(key, movie, self.buckets[index])
        self.count += 1

    # Finds all movie records with the given title or quote.
    def find_all(self, key):
        matches = []
        index = hash_key(key) % TABLE_SIZE
        current = self.buckets[index]
        while current is not None:
            if current.key == key:
                matches.append(current.movie)
            current = current.next
        return matches

    # Counts buckets that have never been used.
    def wasted_space(self):
        empty = 0
        for bucket in self.buckets:
            if bucket is None:
                empty += 1
        return empty


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
    print("ATTEMPT 1: Linked lists with first-letter hash")
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
