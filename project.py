
import myrand
import sys
import math
from process import Process
from cpu import  CPU

def next_exp():
    while True:
        random_num = -math.log(myrand.drand48())/lbd
        if random_num <= upper:
            return random_num


def generate_cpu_bursts():
    random_num = math.ceil(myrand.drand48() * 64)
    cpu_bursts = min(max(random_num, 1), 64)
    return cpu_bursts


def generate_burst_times(is_cpu_bound):
    cpu_burst_time = math.ceil(next_exp())
    io_burst_time = math.ceil(next_exp()) * 10

    if is_cpu_bound:
        cpu_burst_time *= 4
        io_burst_time //= 8

    return cpu_burst_time, io_burst_time


def lats_burst_time(is_cpu_bound):
    cpu_burst_time = math.ceil(next_exp())
    if is_cpu_bound:
        cpu_burst_time *= 4
    return cpu_burst_time


if __name__ == "__main__":
    n = len(sys.argv)
    if n < 6:
        print("Wrong number of command-line arguments", file=sys.stderr)
        exit(1)
    if not sys.argv[1].isdigit():
        print("argv[1] should be a digit", file=sys.stderr)
        exit(1)
    if int(sys.argv[1]) < 1 or int(sys.argv[2]) > 26:
        print("argv[1] should in A-Z", file=sys.stderr)
        exit(1)
    if not sys.argv[2].isdigit():
        print("argv[2] should be a digit", file=sys.stderr)
        exit(1)
    if int(sys.argv[2]) < 0 or int(sys.argv[2]) > int(sys.argv[1]):
        print("Number of CPU bounds processes is wrong", file=sys.stderr)
        exit(1)
    if not sys.argv[3].isdigit():
        print("argv[3] should be a digit", file=sys.stderr)
        exit(1)
    if int(sys.argv[3]) < 0:
        print("Wrong rand seed", file=sys.stderr)
        exit(1)
    try:
        lbd = float(sys.argv[4])  # 1/lbd will be the average random value generated
    except ValueError:
        print("ERROR: argv[4] should be a float", file=sys.stderr)
        exit(1)

    if lbd <= 0:
        print("ERROR: lambda cannot be less than or equal to 0", file=sys.stderr)
        exit(1)

    try:
        upper = float(sys.argv[5])  # the upper bound for valid pseudo-random numbers
    except ValueError:
        print("ERROR: argv[5] should be a float", file=sys.stderr)
        exit(1)
    if not (0 < upper):
        print("ERROR: Illegal upper bound", file=sys.stderr)
        exit(1)

    try:
        tcs = int(sys.argv[6])  # the upper bound for valid pseudo-random numbers
    except ValueError:
        print("ERROR: argv[6] should be a float", file=sys.stderr)
        exit(1)
    if tcs < 0 or tcs % 2 == 1:
        print("ERROR: n_processes should be >= 1 <= 26")
        exit(1)

    try:
        alpha = float(sys.argv[7])  # the upper bound for valid pseudo-random numbers
    except ValueError:
        print("ERROR: argv[7] should be a float", file=sys.stderr)
        exit(1)
    if alpha < 0:
        print("ERROR: n_processes should be >= 1 <= 26")
        exit(1)

    try:
        tslice = int(sys.argv[8])  # the upper bound for valid pseudo-random numbers
    except ValueError:
        print("ERROR: argv[8] should be a int", file=sys.stderr)
        exit(1)
    if tslice < 0:
        print("ERROR: n_processes should be >= 1 <= 26")
        exit(1)


    num_process = int(sys.argv[1])
    num_CPU_bound = int(sys.argv[2])
    random_seed = int(sys.argv[3])
    myrand.srand48(random_seed)
    num_IO_bound = num_process - num_CPU_bound
    CPU_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num_CPU_bound == 1:
        print("<<< PROJECT PART I -- process set (n={}) with 1 CPU-bound process >>>".format(num_process))
    else:
        print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound processes >>>".format(num_process, num_CPU_bound))
    process = []
    process2 = []
    process3 = []
    process4 = []

    for i in range(num_process):
        element = []
        interval = []
        arrive_time = math.floor(next_exp())
        num_cpu_burst = generate_cpu_bursts()
        if i < num_IO_bound:
            print("I/O-bound process {}: arrival time {}ms;".format(CPU_name[i], arrive_time), end=" ")
            if num_cpu_burst == 1:
                print("{} CPU burst:".format(num_cpu_burst))
            else:
                print("{} CPU bursts:".format(num_cpu_burst))
            for j in range(num_cpu_burst-1):
                cpu_burst_time, io_burst_time = generate_burst_times(False)
                interval.append(cpu_burst_time)
                interval.append(io_burst_time)
                print("--> CPU burst {}ms --> I/O burst {}ms".format(cpu_burst_time, io_burst_time))
            cpu_burst_time = lats_burst_time(False)
            print("--> CPU burst {}ms".format(cpu_burst_time))
            interval.append(cpu_burst_time)
            element = Process(arrival_time=arrive_time, cpu_bursts=num_cpu_burst, intervals=interval, io_bound=True, pid=chr(i + ord('A')) )
        else:
            print("CPU-bound process {}: arrival time {}ms;".format(CPU_name[i], arrive_time), end=" ")
            if num_cpu_burst == 1:
                print("{} CPU burst:".format(num_cpu_burst))
            else:
                print("{} CPU bursts:".format(num_cpu_burst))
            for j in range(num_cpu_burst-1):
                cpu_burst_time, io_burst_time = generate_burst_times(True)
                interval.append(cpu_burst_time)
                interval.append(io_burst_time)
                print("--> CPU burst {}ms --> I/O burst {}ms".format(cpu_burst_time, io_burst_time))
            cpu_burst_time = lats_burst_time(True)
            print("--> CPU burst {}ms".format(cpu_burst_time))
            interval.append(cpu_burst_time)
            element = Process(arrival_time=arrive_time, cpu_bursts=num_cpu_burst, intervals=interval, io_bound=False, pid=chr(i + ord('A')) )
        if element:
            process.append(element)
            process2.append(element)
            process3.append(element)
            process4.append(element)
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound {} >>>".format(num_process, num_CPU_bound,
                                                                                     "process" if num_CPU_bound == 1 else "processes"))
    for i in process:
        print(
            "{}-bound process {}: arrival time {}ms; {} CPU bursts:".format("I/O" if i.io_bound else "CPU", i.pid,
                                                                            i.arrival_time, i.cpu_bursts))
    print("\n<<< PROJECT PART II -- t_cs={}ms; alpha={:.2f}; t_slice={}ms >>>".format(tcs, alpha, tslice))

    cpu = CPU(tcs, lbd, alpha)
    cpu.fcfs(process)
    print()
    cpu.shortest_job_first(process2)
    print()
    cpu.shortest_time_remaining(process3)
    print()
    cpu.round_robin(process4, tslice)
