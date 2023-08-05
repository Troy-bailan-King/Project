from copy import deepcopy
from math import ceil


class Process(object):
    def __init__(self, arrival_time: int, cpu_bursts: int, intervals: list, io_bound: bool, pid: str):
        # arrival time in ms
        # number is intervals is cpu bursts * 2 - 1, since every cpu burst is interrupted by an io burst
        # -> processing goes cpu, io, cpu, io, ...., io, cpu

        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts
        self.intervals = deepcopy(intervals)
        self.og_intervals = deepcopy(intervals)
        self.predicted_bursts = list()
        self.intervals_completed = 0
        self.io_bound = io_bound
        self.pid = pid
        self.burst_index = 0
        self.og_predicted_bursts = list()

    def compute_predicted(self, lamda: float, alpha: float):
        for i in range(0, len(self.intervals), 2):
            if i != 0:
                self.predicted_bursts.append(
                    ceil(alpha * self.intervals[i - 2] + (1 - alpha) * self.predicted_bursts[-1]))
            else:
                self.predicted_bursts.append(ceil(1 / lamda))

