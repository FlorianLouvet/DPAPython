from abc import ABCMeta, abstractmethod
from threading import Thread
import numpy as np

from CommonDPA.trace_reading import read_traces


class UnitAttackThread(Thread, metaclass=ABCMeta):
    def __init__(self, values, traces, attacked_unit):
        super(UnitAttackThread, self).__init__()
        self.values = values
        self.unit_values = None
        self.unit_tweaks = None
        self.unit_keys = None
        self.traces = traces
        self.attacked_unit = attacked_unit
        self.key = None

    @abstractmethod
    def extract_unit_values(self):
        pass

    @abstractmethod
    def compute_unit_tweaks(self):
        pass

    @abstractmethod
    def compute_unit_keys(self):
        pass

    def run(self):
        self.extract_unit_values()
        self.compute_unit_tweaks()
        self.compute_unit_keys()

    def result(self):
        assert (self.key is not None)
        return self.key


class DPACommon(metaclass=ABCMeta):
    def __init__(self, traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename):
        super(DPACommon, self).__init__()
        self.cpu_cores = cpu_cores
        self.traces = read_traces(traces_directory, traces_name_prefix, traces_number, cpu_cores)
        self.values = self.read_values(values_filename)
        self.units_number = None
        self.type = None

    def read_values(self, filename):
        with open(filename) as opened_file:
            lines = []
            for i in opened_file.readlines():
                lines += i.split('\r')
        return lines

    @abstractmethod
    def run(self):
        keys = np.reshape(np.zeros(self.units_number, dtype=np.uint8), (self.units_number, 1))
        for j in range(self.units_number // self.cpu_cores):
            threads = []
            for i in range(self.cpu_cores):
                t = self.type(self.values, self.traces, (j * self.cpu_cores) + i + 1)
                t.start()
                threads.append(t)
            for i, t in enumerate(threads):
                t.join()
                keys[(j * self.cpu_cores) + i] = t.result()
        print(keys)

    def run_single_unit(self, attacked_unit):
        t = self.type(self.values, self.traces, attacked_unit)
        t.start()
        t.join()
        print(t.result())
