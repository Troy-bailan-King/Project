import ctypes

# link the rand.so shared library (make sure its in the same directory as myrand.py)
_rand = ctypes.CDLL('./rand.so')

# set the expected argument types for seed() function in the rand.c file
_rand.seed.argtypes = [ctypes.c_long]

# set the return type for the drand() function in the rand.c file
_rand.drand.restype = ctypes.c_double


def srand48(seed: int):
    # call the seed() function
    _rand.seed(ctypes.c_long(seed))
    return


def drand48() -> float:
    # call the drand() function
    return _rand.drand()