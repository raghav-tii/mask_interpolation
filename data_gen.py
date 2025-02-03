import random
import numpy as np


def is_in_boundary_region(x, y, boundary_func, boundary_thickness=0.03):
    if x < -boundary_thickness or x > 1.0+boundary_thickness:
        return False
    return (
        abs(boundary_func(x) - y) < boundary_thickness
        or abs(boundary_func(x) + y) < boundary_thickness
    )


def is_interior(x, y, boundary_func):
    return y < boundary_func(x) and y > -boundary_func(x)


def is_exterior(x, y, boundary_func):
    return y > boundary_func(x) or y < -boundary_func(x)


def boundary_func(x, thickness=0.2):
    if 0.0 <= x <= 1.0:
        airfoil_shape = (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
        y_t = 5 * thickness * airfoil_shape
        return y_t
    else:
        return 0.0


def generate_samples(num_samples, x_range, y_range):
    samples = {"interior": [], "exterior": [], "boundary": []}

    for _ in range(num_samples):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)

        if is_interior(x, y, boundary_func):
            samples["interior"].append((x, y))
        elif is_in_boundary_region(x, y, boundary_func):
            samples["boundary"].append((x, y))
        else:
            samples["exterior"].append((x, y))

    return samples


if __name__ == "__main__":
    num_samples = 10000
    x_range = (-2, 3)
    y_range = (-1, 1)

    samples = generate_samples(num_samples, x_range, y_range)

    print(f"Interior samples: {len(samples['interior'])}")
    print(f"Exterior samples: {len(samples['exterior'])}")
    print(f"Boundary samples: {len(samples['boundary'])}")

    # Save samples to file
    header_str = "x_coordinate,y_coordinate"
    np.savetxt(
        "interior.csv",
        samples["interior"],
        delimiter=",",
        header=header_str,
        fmt="%.6f",
    )
    np.savetxt(
        "exterior.csv",
        samples["exterior"],
        delimiter=",",
        header=header_str,
        fmt="%.6f",
    )
    np.savetxt(
        "boundary.csv",
        samples["boundary"],
        delimiter=",",
        header=header_str,
        fmt="%.6f",
    )
