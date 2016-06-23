from abc import ABCMeta, abstractmethod
from trace_reading import read_traces

class DPACommon(metaclass=ABCMeta):
    def __init__(self, traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename):
        super(DPACommon, self).__init__()
        self.traces = read_traces(traces_directory, traces_name_prefix, traces_number, cpu_cores)
        self.values = self.read_values(values_filename)

    def read_values(self, filename):
        with open(filename) as opened_file:
            lines = []
            for i in opened_file.readlines():
                lines += i.split('\r')
        return lines

    def run(self):
        pass