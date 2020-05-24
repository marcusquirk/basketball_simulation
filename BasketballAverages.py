def average(values):
    """finds the mean of a given list of values"""
    total = 0
    # Find the sum of all the values
    for i in range(len(values)):
        total = total + values[i]
    # Divide by the number of values
    mean = total / len(values)
    return mean


def average_dict(values):
    """finds the mean of a given dictionary of values"""
    total = 0
    for i in values:
        total = total + values[i]
    mean = total / len(values)
    return mean
