from cpa_scream import main as cpa_main
from cpa_scream import read_byte_key
import numpy as np
import argparse
import sys
from glob import glob
from threading import Thread
from MACRO import *
from trace_reading import read_traces


class ByteAttackThread(Thread):
    def __init__(self, value_file, traces, attacked_byte):
        Thread.__init__(self)
        self.value_file = value_file
        self.traces = traces
        self.attacked_byte = attacked_byte
        self.key = None

    def run(self):
        self.key = cpa_main(self.value_file, self.traces, self.attacked_byte)

    def result(self):
        return self.key


def main(number_of_traces, traces_input_file_format, trace_name_prefix, value_file, cores):
    print("KEY USED FOR TRACES: {}".format(read_byte_key(DEFAULT_KEY_INPUT)))
    traces = read_traces(traces_input_file_format, trace_name_prefix, number_of_traces, cores)
    keys = np.reshape(np.zeros(BYTES_IN_PLAINTEXT, dtype=np.uint8), (BYTES_IN_PLAINTEXT, 1))
    threads = []
    for i in range(BYTES_IN_PLAINTEXT):
        t = ByteAttackThread(value_file, traces, i + 1)
        t.start()
        threads.append(t)
    for i, t in enumerate(threads):
        t.join()
        keys[i] = t.result()
    print(keys)
    # keys = np.unpackbits(keys, axis=1)
    # print(keys)
    # keys = np.rot90(keys)
    # print(keys)
    # (pair_bytes, odd_bytes) = np.hsplit(keys, 2)
    # pair_bytes = np.packbits(pair_bytes)
    # odd_bytes = np.packbits(odd_bytes)
    # print(pair_bytes)
    # print(odd_bytes)
    # key = np.vstack((odd_bytes, pair_bytes)).reshape((-1,), order='F')
    # print(key)
    # np.set_printoptions(formatter={'int': hex})
    # print(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbosity", action="store_true", help="increase output verbosity")
    parser.add_argument("-vi", "--init_input_file",
                        dest="value_file", action="store", default=DEFAULT_VALUES_INPUT)
    parser.add_argument(
        "-ti", "--input", action="store", dest='trace_input', default=DEFAULT_TRACES_INPUT)
    parser.add_argument(
        '-tnp', '--name_prefix', dest='trace_name_prefix', default=DEFAULT_TRACE_NAME_PREFIX)
    parser.add_argument(
        '-tn', "--number_of_traces", dest="number_of_traces", default=None, type=int)
    parser.add_argument(
        '-c', "--cores", dest="number_of_cores", default=4, type=int)

    args = parser.parse_args()
    if not args.verbosity:
        f = open('/dev/null', 'w')
        sys.stdout = f
    if args.number_of_traces is None:
        number_of_traces = len(glob(args.trace_input + '*.bin'))
    else:
        number_of_traces = args.number_of_traces
    main(number_of_traces, args.trace_input, args.trace_name_prefix,
         args.value_file, args.number_of_cores)
