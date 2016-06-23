import numpy as np
import argparse
import sys
from glob import glob
from MACRO import *
from trace_reading import read_traces

SCREAM_SBOX = {0: 32, 1: 141, 2: 178, 3: 218, 4: 51, 5: 53, 6: 166, 7: 255, 8: 122, 9: 82, 10: 106, 11: 198, 12: 164,
               13: 168, 14: 81, 15: 35, 16: 162, 17: 150, 18: 48, 19: 171, 20: 200, 21: 23, 22: 20, 23: 158, 24: 232,
               25: 243, 26: 248, 27: 221, 28: 133, 29: 226, 30: 75, 31: 216, 32: 108, 33: 1, 34: 14, 35: 61, 36: 182,
               37: 57, 38: 74, 39: 131, 40: 111, 41: 170, 42: 134, 43: 110, 44: 104, 45: 64, 46: 152, 47: 95, 48: 55,
               49: 19, 50: 5, 51: 135, 52: 4, 53: 130, 54: 49, 55: 137, 56: 36, 57: 56, 58: 157, 59: 84, 60: 34,
               61: 123, 62: 99, 63: 189, 64: 117, 65: 44, 66: 71, 67: 233, 68: 194, 69: 96, 70: 67, 71: 172, 72: 87,
               73: 161, 74: 31, 75: 39, 76: 231, 77: 173, 78: 92, 79: 210, 80: 15, 81: 119, 82: 253, 83: 8, 84: 121,
               85: 58, 86: 73, 87: 93, 88: 237, 89: 144, 90: 101, 91: 124, 92: 86, 93: 79, 94: 46, 95: 105, 96: 205,
               97: 68, 98: 63, 99: 98, 100: 91, 101: 136, 102: 107, 103: 196, 104: 94, 105: 45, 106: 103, 107: 11,
               108: 159, 109: 33, 110: 41, 111: 42, 112: 214, 113: 126, 114: 116, 115: 224, 116: 65, 117: 115, 118: 80,
               119: 118, 120: 85, 121: 151, 122: 60, 123: 9, 124: 125, 125: 90, 126: 146, 127: 112, 128: 132, 129: 185,
               130: 38, 131: 52, 132: 29, 133: 129,
               134: 50, 135: 43, 136: 54, 137: 100, 138: 174, 139: 192, 140: 0, 141: 238, 142: 143, 143: 167, 144: 190,
               145: 88, 146: 220, 147: 127, 148: 236, 149: 155, 150: 120, 151: 16, 152: 204, 153: 47, 154: 148,
               155: 241, 156: 59, 157: 156, 158: 109, 159: 22, 160: 72, 161: 181, 162: 202, 163: 17, 164: 250, 165: 13,
               166: 142, 167: 7, 168: 177, 169: 12, 170: 18, 171: 40, 172: 76, 173: 70, 174: 244, 175: 139, 176: 169,
               177: 207, 178: 187, 179: 3, 180: 160, 181: 252, 182: 239, 183: 37, 184: 128, 185: 246, 186: 179,
               187: 186, 188: 62, 189: 247, 190: 213, 191: 145, 192: 195, 193: 138, 194: 193, 195: 69, 196: 222,
               197: 102, 198: 245, 199: 10, 200: 201, 201: 21, 202: 217, 203: 163, 204: 97, 205: 153, 206: 176,
               207: 228, 208: 209, 209: 251, 210: 211, 211: 78, 212: 191, 213: 212, 214: 215, 215: 113, 216: 203,
               217: 30, 218: 219, 219: 2, 220: 26, 221: 147, 222: 234, 223: 197, 224: 235, 225: 114, 226: 249, 227: 28,
               228: 229, 229: 206, 230: 77, 231: 242, 232: 66, 233: 25, 234: 225, 235: 223, 236: 89, 237: 149, 238: 183,
               239: 140, 240: 154, 241: 240, 242: 24, 243: 230, 244: 199, 245: 175, 246: 188, 247: 184, 248: 227,
               249: 27, 250: 208, 251: 165, 252: 83, 253: 180, 254: 6, 255: 254}


def valid_byte(input_string):
    value = int(input_string)
    if value < 1 or value > BYTES_IN_PLAINTEXT:
        raise argparse.ArgumentTypeError()
    return value


def read_byte_key(input_filename):
    with open(input_filename) as opened_file:
        key_string = opened_file.readline()
        key = []
        for i in range(1, 17):
            attacked_byte = i
            key += [int(format(int(key_string, 16), '#0130b')[2:][
                        ((attacked_byte - 1) % BYTE)::BYTE][::-1][(attacked_byte - 1) // 8::2], 2)]
    return np.array(key)


def read_values(input_filename, attacked_byte):
    with open(input_filename) as opened_file:
        lines = []
        for i in opened_file.readlines():
            lines += i.split('\r')
        values = [int(format(int(line, 16), '#0130b')[2:][
                      ((attacked_byte - 1) % BYTE)::BYTE][::-1][(attacked_byte - 1) // 8::2], 2) for line in lines]
    return np.array(values)


def get_keys(bit_length):
    return np.arange(0, 2 ** bit_length)


def compute_cutted_tweaks(size, attacked_byte):
    matrix = np.zeros(size, dtype=int)
    nonce = 1
    for tweak in np.nditer(matrix, op_flags=['readwrite']):
        tweak = format(nonce, '#090b')[
                2:] + format(16, '#010b')[2:] + format(0, '#034b')[2:]
        tweak = int(tweak[((attacked_byte - 1) % BYTE)::BYTE]
                    [::-1][(attacked_byte - 1) // 8::2], 2)
        nonce += 1
    return matrix


def compute_intermediate_values(initial_values, key_hypotheses, tweaks):
    matrix = np.zeros(
        (np.size(initial_values), np.size(key_hypotheses)), dtype=np.int)
    shape = np.shape(matrix.shape)
    it = np.nditer(matrix, flags=['multi_index'], op_flags=['writeonly'])
    while not it.finished:
        it[0] = SCREAM_SBOX[initial_values[it.multi_index[0]] ^ key_hypotheses[
            it.multi_index[1]] ^ tweaks[it.multi_index[0]]]
        it.iternext()
    return matrix


def bitsoncount(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24


def model_intermediate_values(intermediate_values):
    v_hamming_weight_comp = np.vectorize(bitsoncount)
    return v_hamming_weight_comp(intermediate_values)


def compute_correlation(simulated_consumption, traces):
    h_mean = np.mean(simulated_consumption, axis=0)
    t_mean = np.mean(traces, axis=0)
    h_sums = np.sum(simulated_consumption, axis=0)
    t_sums = np.sum(traces, axis=0)
    h_sums_square = np.sum(simulated_consumption ** 2, axis=0)
    h_mean_square = simulated_consumption.shape[0] * (h_mean ** 2)
    t_sums_square = np.sum(traces ** 2, axis=0)
    t_mean_square = traces.shape[0] * (t_mean ** 2)

    outer_hmean_tsum = np.outer(h_mean, t_sums)
    outer_hsums_tmean = np.outer(h_sums, t_mean)
    outer_hmean_tmean = np.outer(
        h_mean, t_mean) * simulated_consumption.shape[0]

    h_square_sum = h_sums_square + h_mean_square - (2 * h_mean * h_sums)
    t_square_sum = t_sums_square + t_mean_square - (2 * t_mean * t_sums)
    time_square_root = np.sqrt(np.outer(h_square_sum, t_square_sum))

    matrix = (-outer_hmean_tsum - outer_hsums_tmean + outer_hmean_tmean +
              np.dot(simulated_consumption.T, traces)) / time_square_root
    return matrix


def pretty_results():
    pass


def main(init_filename, T_MATRIX, attacked_byte, correlation_output=False):
    print("Getting initial values...")
    values = read_values(init_filename, attacked_byte)
    print("Getting keys hypothesis...")
    byte_keys = get_keys(BYTE)
    values = values[:T_MATRIX.shape[0]]
    print("Computing tweak")
    TWEAKS = compute_cutted_tweaks(T_MATRIX.shape[0], attacked_byte)
    print("Computing intermediate values...")
    V_MATRIX = compute_intermediate_values(values, byte_keys, TWEAKS)
    print("Computing consumption hypothesis...")
    H_MATRIX = model_intermediate_values(V_MATRIX)
    print("Computing correlation")
    R_MATRIX = compute_correlation(H_MATRIX, T_MATRIX)
    # if correlation_output:
    #     np.savetxt("correlation.bin", R_MATRIX.T, delimiter=" ", fmt="%.4f")
    oned_indice = np.argmax(R_MATRIX)
    print(oned_indice // R_MATRIX.shape[1])
    print(oned_indice % R_MATRIX.shape[1])
    # print(R_MATRIX[oned_indice//R_MATRIX.shape[1]]
    #       [oned_indice % R_MATRIX.shape[1]])
    # print(np.mean(np.absolute(R_MATRIX)))
    # print(np.percentile(np.absolute(R_MATRIX), 25))
    # print(np.percentile(np.absolute(R_MATRIX), 90))
    print((np.argsort(R_MATRIX, axis=None) % R_MATRIX.shape[1])[-20:])
    # print(np.sort(R_MATRIX, axis=None))
    return oned_indice // R_MATRIX.shape[1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbosity", action="store_true", help="increase output verbosity")
    parser.add_argument("-vi", "--init_input_file",
                        dest="init_filename", action="store", default=DEFAULT_VALUES_INPUT)
    parser.add_argument("-a", "--attacked_byte", action="store",
                        default=1, type=valid_byte, dest="attacked_byte")
    parser.add_argument(
        "-ti", "--input", action="store", dest='trace_input', default=DEFAULT_TRACES_INPUT)
    parser.add_argument(
        '-tnp', '--name_prefix', dest='name_prefix', default=DEFAULT_TRACE_NAME_PREFIX)
    parser.add_argument(
        '-tn', "--number_of_traces", dest="number_of_traces", default=None, type=int)
    parser.add_argument(
        '-o', "--correlation_output", action="store_true", dest="correlation_output", default=False)
    parser.add_argument(
        '-c', "--cores", action="store", dest="cores_number", default=4, type=int)

    args = parser.parse_args()
    if not args.verbosity:
        f = open('/dev/null', 'w')
        sys.stdout = f
    if args.number_of_traces is None:
        number_of_traces = len(glob(args.input + '*.bin'))
    else:
        number_of_traces = args.number_of_traces
    traces = read_traces(number_of_traces, args.trace_input, args.name_prefix, args.cores)
    main(args.init_filename, traces,
         args.attacked_byte, args.correlation_output)
