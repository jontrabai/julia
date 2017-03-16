"""
Julia set generator without option PIL-based image drawing
"""
import time
from functools import wraps
from memory_profiler import profile


# area of a complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("@timefn:", fn.__name__, "took", str(t2 - t1), "seconds.")
        return result
    return measure_time


def calc_pure_python(desired_width, max_iterations):
    """
    Create a list of complex coordinates (zs) and complex
    parameters (cs), build a Julia set, and display it
    :param desired_width: width of the set
    :param max_iterations: max iterations
    :return: returns nothing
    """
    x_step = (float(x2 - x1) / float(desired_width))
    y_step = (float(y1 - y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    # Build a list of coordinates and the initial condition of each cell.
    # Note that our initial condition is a constant and could easily be removed;
    # we us it to simulate a real-world scenario with several inputs to
    # our funcion.
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))
    print("Length of x:", len(x))
    print("Total elements:", len(zs))
    output = calculate_z_serial_pure_python(max_iterations, zs, cs)

    # This sum is expected for a 1000 square grid with 300 iterations
    # It catches minor errors we might intoduce when we're working on
    # a fixed seet of inputs
    assert sum(output) == 33219980

@profile
def calculate_z_serial_pure_python(maxiter, zs, cs):
    """
    Calculate output list using Julia update rule
    :param maxiter:  max iterations
    :param zs: zs
    :param cs: cs
    :return: the output
    """
    output = [0] * len(zs)
    time.sleep(1)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


if __name__ == '__main__':
    # Calculate the Julia set using a pure Python solution with
    # reasonable defaults for a laptop
    calc_pure_python(desired_width=1000, max_iterations=300)
