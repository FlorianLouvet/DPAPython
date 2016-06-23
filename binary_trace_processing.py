import struct

def read_trace_from_bin(filename, start=0, stop=None, step=1):

    CHAR = 1
    UNSIGNED = 4
    FLOAT = 4
    DOUBLE = 8

    int_b = lambda b: int.from_bytes(b, byteorder='little')
    float_b = lambda b: struct.unpack('f', b)[0]
    double_b = lambda b: struct.unpack('d', b)[0]

    with open(filename, 'rb') as f:

        for _ in range(6):
            b = f.read(UNSIGNED)

        points_nbr = f.read(UNSIGNED)
        avg_count = f.read(UNSIGNED)

        x_disp_range = f.read(FLOAT)
        x_disp_org = f.read(DOUBLE)
        x_incr = f.read(DOUBLE)
        x_origin = f.read(DOUBLE)

        for _ in range(6):
            b = f.read(CHAR)
            while chr(ord(b)) != '\0':
                b = f.read(CHAR)

        for _ in range(21):
            b = f.read(CHAR)
            while chr(ord(b)) != '\0':
                b = f.read(CHAR)

        b = f.read(CHAR)
        while b != b'\x0c':
            b = f.read(CHAR)

        b = f.read(CHAR)
        while b != b'\x01':
            b = f.read(CHAR)

        b = f.read(CHAR)
        while b != b'\x04':
            b = f.read(CHAR)

        f.read(CHAR)
        whateverthisis = int_b(f.read(UNSIGNED))

        trace = []
        if stop == None or stop > int_b(points_nbr):
            stop = int_b(points_nbr)

        for _ in range(start, stop, step):
            trace.append(float_b(f.read(FLOAT)))
        return trace
