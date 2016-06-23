import numpy as np
from abc import ABCMeta, abstractmethod


class DPAUnitAttcack(metaclass=ABCMeta):
    def __init__(self, traces, values, keys, tweaks):
        super(DPAUnitAttcack, self).__init__()
        self.traces = traces
        self.values = values
        self.keys = keys
        self.tweaks = tweaks
        self.v_hamming_weight_comp = np.vectorize(self.hamming_weight)
        self.intermediate_values_matrix = None
        self.simulated_power_consumption_matrix = None

    def hamming_weight(self, value):
        value = value - ((value >> 1) & 0x55555555)
        value = (value & 0x33333333) + ((value >> 2) & 0x33333333)
        return (((value + (value >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

    def simulate_power_consumption(self):
        self.simulated_power_consumption_matrix = self.v_hamming_weight_comp(self.intermediate_values_matrix)

    def compute_correlation_matrix(self):
        h_mean = np.mean(self.simulated_power_consumption_matrix, axis=0)
        t_mean = np.mean(self.traces, axis=0)
        h_sums = np.sum(self.simulated_power_consumption_matrix, axis=0)
        t_sums = np.sum(self.traces, axis=0)
        h_sums_square = np.sum(self.simulated_power_consumption_matrix ** 2, axis=0)
        h_mean_square = self.simulated_power_consumption_matrix.shape[0] * (h_mean ** 2)
        t_sums_square = np.sum(self.traces ** 2, axis=0)
        t_mean_square = self.traces.shape[0] * (t_mean ** 2)

        outer_hmean_tsum = np.outer(h_mean, t_sums)
        outer_hsums_tmean = np.outer(h_sums, t_mean)
        outer_hmean_tmean = np.outer(
            h_mean, t_mean) * self.simulated_power_consumption_matrix.shape[0]

        h_square_sum = h_sums_square + h_mean_square - (2 * h_mean * h_sums)
        t_square_sum = t_sums_square + t_mean_square - (2 * t_mean * t_sums)
        time_square_root = np.sqrt(np.outer(h_square_sum, t_square_sum))

        matrix = (-outer_hmean_tsum - outer_hsums_tmean + outer_hmean_tmean +
                  np.dot(self.simulated_power_consumption_matrix.T, self.traces)) / time_square_root
        return matrix

    @abstractmethod
    def compute_intermediate_values_matrix(self):
        pass

    def run(self):
        self.compute_intermediate_values_matrix()
        self.simulate_power_consumption()
        self.compute_correlation_matrix()
