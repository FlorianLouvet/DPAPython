from binary_trace_processing import read_trace_from_bin
from threading import Thread
import numpy as np


class TraceThread(Thread):
    def __init__(self, sta, stop, buffer, directory, name_prefix):
        Thread.__init__(self)
        self.sta = sta
        self.stop = stop
        self.buffer = buffer
        self.directory = directory
        self.name_prefix = name_prefix

    def run(self):
        self.buffer = read_some_traces(
            self.sta, self.stop, self.buffer, self.directory, self.name_prefix)

    def result(self):
        return self.buffer


def read_some_traces(sta, stop, buffer, directory, name_prefix):
    for i in range(sta, stop + 1):
        print("\t" + name_prefix + str(i))
        buffer = np.vstack(
            (buffer, read_trace_from_bin(directory + name_prefix + str(i) + '.bin')))
    return buffer


def read_traces(directory, name_prefix, number, cpu_cores):
    print("Reading collected traces...")

    ranges = np.array_split(np.arange(number), cpu_cores)
    buffers = []

    for i in range(cpu_cores):
        print("\t" + name_prefix + str(ranges[i][0]))
        buffers.append(np.array(
            read_trace_from_bin(directory + name_prefix + str(ranges[i][0]) + '.bin')))

    threads = []
    for i, r in enumerate(ranges):
        t = TraceThread(
            r[1], r[-1], buffers[i], directory, name_prefix)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    traces = threads[0].result()
    for t in threads[1:]:
        traces = np.vstack((traces, t.result()))
    return traces
