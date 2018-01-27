from parsing import read_instance
from solution import astar
from sys import argv

if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage: python3 run_astar.py <instance>")
    instance = read_instance(argv[1])
    path = astar(*instance)
    if not path:
        print("No solution found.")
    else:
        print("Path:", ", ".join(str(i) for i in path))