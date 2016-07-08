from CommonDPA.dpa_unit_attack import *


class PrimateUnitAttack(DPAUnitAttcack):
    SBOX = {0: 1, 1: 0, 2: 25, 3: 26, 4: 17, 5: 29, 6: 21, 7: 27, 8: 20, 9: 5, 10: 4, 11: 23, 12: 14, 13: 18, 14: 2,
            15: 28, 16: 15, 17: 8, 18: 6, 19: 3, 20: 13, 21: 7, 22: 24, 23: 16, 24: 30, 25: 9, 26: 31, 27: 10, 28: 22,
            29: 12, 30: 11, 31: 19}

    def __init__(self, traces, values, keys, tweaks):
        super(PrimateUnitAttack, self).__init__(traces, values, keys, tweaks)

    def compute_intermediate_values_matrix(self):
        matrix = np.zeros(
            (np.size(self.values), np.size(self.keys)), dtype=np.int)
        it = np.nditer(matrix, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = PrimateUnitAttack.SBOX[self.keys[it.multi_index[1]]]
            it.iternext()
        self.intermediate_values_matrix = matrix
