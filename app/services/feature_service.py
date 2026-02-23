import numpy as np

def compute_acwr(acute, chronic):
    if chronic == 0:
        return 0
    return acute/ chronic

def compute_monotony(loads):
    mean = np.mean(loads)
    std = np.std(loads)
    if std == 0:
        return 0
    return mean/std