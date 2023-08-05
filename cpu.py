from process import Process
from heapq import *


class CPU:

    def __init__(self, context_switch_time: int, lamda: float, alpha: float):
        self.__tcs__ = context_switch_time
        self.__arrivalqueue__ = []
        self.lamda = lamda
        self.alpha = alpha
        self.time = 0
        self.time_in_cpu = 0
        self.state = {}
        # Stores ready time, entry time, and exit time for each process
        self.preemption = 0
        self.simout = open("simout.txt", "w")

    def __printreadyqueueFCFS__(self, ready_que: list):
        if len(ready_que) != 0:
            return "[Q " + " ".join([p.pid for p in ready_que]) + "]"
        return "[Q <empty>]"

    def get_next_arrivals(self, arrival_q):
        next_arrivals = []
        next_arrival_time = arrival_q[-1].arrival_time
        while len(arrival_q) > 0 and arrival_q[-1].arrival_time == next_arrival_time:
            next_arrivals.append(arrival_q.pop())
        return next_arrivals