import math


def get_temp(minute, second, subsecond):
    t = (minute*60.0) + second + (subsecond/1024.0)
    w = 2 * math.pi * (1/1200)
    return int((math.sin(w*t) * (((2**12)-1)/2)) + (((2**12)-1)/2))


def get_pressure(minute, second, subsecond):
    t = (minute*60.0) + second + (subsecond/1024.0)
    w = 2 * math.pi * (2/1200)
    return int((math.sin(w*t) * (((2**12)-1)/2)) + (((2**12)-1)/2))


def get_acc(minute, second, subsecond):
    t = (minute*60.0) + second + (subsecond/1024.0)
    w = 2 * math.pi * (3/1200)
    return int((math.sin(w*t) * (((2**16)-1)/2)) + (((2**16)-1)/2))


def get_payload(minute, second, subsecond):
    t = (minute*60.0) + second + (subsecond/1024.0)
    w = 2 * math.pi * (4/1200)
    return int((math.sin(w*t) * (((2**16)-1)/2)) + (((2**16)-1)/2))

# Trame :
# 32 | 12    | 32 | 12    | 32 | 12       | 32 | 16   | 32 | 16   | 32 | 16      | + 4 = 280 = 35 * 8bits
# t1 | temp1 | t2 | temp2 | t3 | pression | t4 | acc1 | t5 | acc2 | t6 | payload |

# Current
# 32 | 12    | 32 | 12       | 32 | 16   | 32 | 16      | = 184 = 23 * 8bits
# t1 | temp1 | t3 | pression | t4 | acc1 | t6 | payload |


def generate_data(duration):
    result = ""

    subsecond = 0.0
    second = 0
    minute = 0

    freq = 20  # Hz

    num_steps = duration*freq

    for i in range(0, num_steps):
        frame = ""

        # timestamp
        frame += f"{minute:08b}"
        frame += f"{second:08b}"
        frame += f"{int(subsecond*1024):016b}"

        frame += f"{get_temp(minute, second, subsecond):012b}"

        # timestamp
        frame += f"{minute:08b}"
        frame += f"{second:08b}"
        frame += f"{int(subsecond*1024):016b}"

        frame += f"{get_pressure(minute, second, subsecond):012b}"

        # timestamp
        frame += f"{minute:08b}"
        frame += f"{second:08b}"
        frame += f"{int(subsecond*1024):016b}"

        frame += f"{get_acc(minute, second, subsecond):016b}"

        # timestamp
        frame += f"{minute:08b}"
        frame += f"{second:08b}"
        frame += f"{int(subsecond*1024):016b}"

        frame += f"{get_payload(minute, second, subsecond):016b}"

        # add it to the result
        result += frame

        # update time
        subsecond += (1/freq)  # periode

        if subsecond >= 1.0:
            second += 1
            subsecond = 0
        if second >= 60:
            minute += 1
            second = 0
        if minute >= 60:
            minute = 0
    
    print("Size of eeprom content:", len(result))
    return result  # binary string
