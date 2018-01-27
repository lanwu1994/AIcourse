import random
from copy import deepcopy
import time

last_parsed = ("", None)

def read_instance(filename):
    global last_parsed
    if filename == last_parsed[0]:
        return last_parsed[1]
    data = {}
    n = 0
    t = time.time()
    data["start"] = data["goal"] = 0
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("nodes"):
                n = int(line[6:-3])
                adj = [[] for i in range(n+1)]
                coords = [None for i in range(n+1)]
            elif line.startswith("vertex"):
                i,x,y = [int(i) for i in line[7:-3].split(",")]
                coords[i] = (x,y)
            elif line.startswith("arc"):
                x,y,d = [int(i) for i in line[4:-3].split(",")]
                adj[x].append((y,d))
            elif line.startswith("start") or line.startswith("goal"):
                line = line.strip()
                head = line.split("(")[0]
                args = line.split("(")[1].split(")")[0].split(",")
                data[head] = int(args[0])
    if not data["start"]:
        data["start"] = 1
    if not data["goal"]: 
        data["goal"] = n
    start = data["start"]
    goal = data["goal"]
    
    t1 = time.time()
    retval = (coords, adj, start, goal)
    last_parsed = (filename, retval)
    return deepcopy(retval)
    #print("Parsing overhead: %.02f seconds." % (t1 - t))
            