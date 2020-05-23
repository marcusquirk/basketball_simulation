class BasketballAverages:

    def average(self, values):
        """finds the mean of a given list of values"""
        total = 0
        # Find the sum of all the values
        for i in range(len(values)):
            total = total + values[i]
        # Divide by the number of values
        average = total / len(values)
        return average

    def average_dict(self, values):
        """finds the mean of a given dictionary of values"""
        total = 0
        for i in values:
            total = total + values[i]
        average = total / len(values)
        return average
