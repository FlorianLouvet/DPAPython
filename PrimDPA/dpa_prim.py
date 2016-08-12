from CommonDPA.dpa_common import UnitAttackThread, DPACommon
from PrimDPA.parameters import *
from PrimDPA.prim_unit_attack import *


class PrimUnitAttackThread(UnitAttackThread):
    def __init__(self, values, traces, attacked_unit):
        super(PrimUnitAttackThread, self).__init__(values, traces, attacked_unit)

    def extract_unit_values(self):
        self.unit_values = np.ones(len(self.values))

    def compute_unit_tweaks(self):
        pass

    def compute_unit_keys(self):
        self.unit_keys = np.arange(0, 2 ** ELEMENT)

    def run(self):
        super(PrimUnitAttackThread, self).run()
        print("Running attack on unit: {}".format(self.attacked_unit))
        self.key = PrimateUnitAttack(self.traces, self.unit_values, self.unit_keys, self.unit_tweaks).run()


class DPAPrim(DPACommon):
    def __init__(self, traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename):
        super(DPAPrim, self).__init__(traces_directory, traces_name_prefix, traces_number, cpu_cores, values_filename)
        self.type = PrimUnitAttackThread
        self.units_number = int(ELEMENTS_IN_BLOCK)

    def run(self):
        super(DPAPrim, self).run()
