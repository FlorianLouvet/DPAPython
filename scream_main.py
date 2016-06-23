import argparse
import sys
from glob import glob
from MACRO import *
from dpa_scream import DPAScream

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
    DPAScream(args.trace_input, args.trace_name_prefix, number_of_traces, args.number_of_cores, args.value_file).run()
