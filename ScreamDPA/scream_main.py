import argparse
import sys
from glob import glob

from ScreamDPA.dpa_scream import DPAScream
from ScreamDPA.parameters import *

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
    parser.add_argument(
        '-su', "--single_unit", dest="single_unit", default=None, type=int)

    args = parser.parse_args()
    if not args.verbosity:
        f = open('/dev/null', 'w')
        sys.stdout = f
    if args.number_of_traces is None:
        number_of_traces = len(glob(args.trace_input + '*.bin'))
    else:
        number_of_traces = args.number_of_traces
    if (args.single_unit is None):
        DPAScream(args.trace_input, args.trace_name_prefix, number_of_traces, args.number_of_cores,
                  args.value_file).run()
    else:
        assert(args.single_unit > 0 and args.single_unit < BYTES_IN_PLAINTEXT+1)
        DPAScream(args.trace_input, args.trace_name_prefix, number_of_traces, args.number_of_cores,
                  args.value_file).run_single_unit(args.single_unit)
