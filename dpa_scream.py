from dpa_common import UnitAttackThread, DPACommon
from MACRO import *
from scream_unit_attack import *


class ScreamUnitAttackThread(UnitAttackThread):
    def __init__(self, values, traces, attacked_unit):
        super(ScreamUnitAttackThread, self).__init__(values, traces, attacked_unit)

    def extract_unit_values(self):
        self.unit_values = np.array([int(format(int(line, 16), '#0130b')[2:][
                                         ((self.attacked_unit - 1) % BYTE)::BYTE][::-1][
                                         (self.attacked_unit - 1) // 8::2], 2) for line in self.values])[
                           :self.traces.shape[0]]

    def compute_unit_tweaks(self):
        matrix = np.zeros(self.traces.shape[0], dtype=int)
        nonce = 1
        for tweak in np.nditer(matrix, op_flags=['readwrite']):
            tweak = format(nonce, '#090b')[
                    2:] + format(16, '#010b')[2:] + format(0, '#034b')[2:]
            tweak = int(tweak[((self.attacked_unit - 1) % BYTE)::BYTE]
                        [::-1][(self.attacked_unit - 1) // 8::2], 2)
            nonce += 1
        self.unit_tweaks = matrix

    def compute_unit_keys(self):
        self.unit_keys = np.arange(0, 2 ** BYTE)

    def run(self):
        super(ScreamUnitAttackThread, self).run()
        print("Running attack on unit: {}".format(self.attacked_unit))
        self.key = ScreamUnitAttack(self.traces, self.unit_values, self.unit_keys, self.unit_tweaks).run()


class DPAScream(DPACommon):
    def __init__(self, traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename):
        super(DPAScream, self).__init__(traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename)
        self.type = ScreamUnitAttackThread
        self.units_number = int(BYTES_IN_PLAINTEXT)

    def run(self):
        super(DPAScream, self).run()
