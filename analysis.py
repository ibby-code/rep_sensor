from ast import literal_eval
from enum import Enum
from statistics import variance

DEFAULT_FILE = 'C:/Users/ibbya/Documents/recurse/rep_sensor/recordings/one_set_of_ten.txt'

class Column(Enum):
    Accel = 0
    Gyro = 1
    Quarternion = 2
    LinearAccel = 3
    Gravity = 4

class Axis(Enum):
    X = 0
    Y = 1
    Z = 2
    W = 3

def load(filename):
    with open(filename, "r") as f:
        headers = f.readline().strip().split(":")
        data = {h:[] for h in headers}
        line = f.readline()
        while line != "":
            line_values = line.split(":")
            for i in range(len(line_values)):
                # each value is a tuple of floats as a string
                try:
                    val = [float(x.strip("()\n")) for x in line_values[i].split(",")]
                    data[headers[i]].append(val)
                except:
                    print(line_values)
            line = f.readline()
        return data

def find_greatest_variance_axis(data):
    """Return axis with greatest variance from array of [x,y,z]"""
    x_values = [row[0] for row in data]
    y_values = [row[1] for row in data]
    z_values = [row[2] for row in data]
    x_var = variance(x_values)
    y_var = variance(y_values)
    z_var = variance(z_values)
    max_var = max(x_var, y_var, z_var)
    if max_var == x_var:
        return (Axis.X, x_values)
    elif max_var == y_var:
        return (Axis.Y, y_values)
    if max_var == z_var:
        return (Axis.Z, z_values)

def is_turning_point(data, i):
    """Compare to two consecutive points to the left and two to the right"""
    if i < 2 or i + 2 >= len(data):
        return False
    point = data[i]
    neigbor_points = data[i-2:i] + data[i+1: i+3]
    is_min = all([x > point for x in neigbor_points])
    is_max = all([x < point for x in neigbor_points])
    return is_min or is_max

def rep_counting_algo(data, column):
    """Count any pair of turning points that have a distance over the threshold"""
    (axis, axis_data) = find_greatest_variance_axis(data[column])
    c = 0
    threshold = (max(axis_data) - min(axis_data))/2
    turning_points = []
    for i in range(len(axis_data)):
        if is_turning_point(axis_data, i):
            turning_points.append(axis_data[i])
        if len(turning_points) == 3:
            height_a = abs(turning_points[0] - turning_points[1])
            height_b = abs(turning_points[1] - turning_points[2])
            rep_height = height_a + height_b
            if rep_height > threshold:
                c += 1
                turning_points = turning_points[3:]
            else:
                turning_points.pop(0)
    return c

def calculate(filename):
    data = load(filename)
    grav_count = rep_counting_algo(data, Column.Gravity.name)
    #gyro_count = rep_counting_algo(data, Column.Gyro.name)
    a_count = rep_counting_algo(data, Column.Accel.name)
    la_count = rep_counting_algo(data, Column.LinearAccel.name)
    return (
        f"Grav count: {grav_count}\n"
    #    f"Gyro count: {gyro_count}\n"
        f"Accel count: {a_count}\n"
        f"LinearAccel count: {la_count}\n" 
    )


    return  

if __name__ == "__main__":
    import sys
    if not len(sys.argv) > 1:
        arg = DEFAULT_FILE
    else:
        arg = sys.argv[1]
    print(calculate(arg))
