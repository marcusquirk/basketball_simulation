class Imperial:
    """This class defines how to represent length in feet and inches"""

    def __init__(self, feet, inches):
        """Stores feet and inches"""

        # Feet must be an integer. Include extra inches over 12
        self.feet = int(feet + (inches // 12))
        # Inches can be stored up to three decimal places
        self.inches = round(inches % 12, 3)

    def __str__(self):
        """"The string returns the standard way of representing feet and inches.
        6ft 7in would be represented as 6'7"."""
        return str(self.feet) + "'" + str(self.inches) + '"'


def from_metric(length):
    """Converts a length from cm to feet and inches."""
    return Imperial(0, length / 2.54)


def from_metric_round(length, decimal):
    """Converts a length from cm to feet and inches, and rounds
    to the given number of decimal places."""
    if decimal == 0:
        return Imperial(0, int(length / 2.54))
    else:
        return Imperial(0, round(length / 2.54, decimal))
