import numpy as np

def duplicated(list):
    u, c = np.unique(list, return_counts=True)
    dup = u[c > 1]
    print(dup)
    return dup

def sum(dup):
    return len(dup)
