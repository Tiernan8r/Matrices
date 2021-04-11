import math

import Matrix


class Vector(object):
    """A Vector class to be used in rows of the Matrix, or just as a General Vector class"""

    # The entries in the Vector
    entries = []

    def __init__(self, values: list):

        """Create a new Vector taking in an arbitrary amount of numerical entries as the values in the vector"""
        # Convert the given tuple to a list:
        values = list(values)

        if isinstance(values[0], list):
            values = values[0]

        # If the values list is actually only storing a vector, inherit it's
        # values:
        if isinstance(values[0], Vector):
            vector = values[0]
            self.entries = vector.entries
            return

        # Iterate over all given values and make sure they are floats
        for i in range(len(values)):
            values[i] = float(values[i])
        self.entries = values

    def __len__(self):
        """Return the number of entries in the Vector"""
        return len(self.entries)

    def __getitem__(self, i):
        """Get the entry at index i of the Vector"""
        # If the index is out of range, raise an indexing error
        if not self.index_in_range(i):
            raise IndexError()
        # Otherwise return the value
        return self.entries[i]

    def __setitem__(self, i, value):
        """Set the item at index i to the given value, as long as it is numerical"""
        # Make sure the index is not out of range
        if not self.index_in_range(i):
            raise IndexError()
        # Make sure the value is numerical
        try:
            value = float(value)
        except ValueError:
            raise ValueError("Cannot assign a non numerical value to a vector")

        self.entries[i] = value

    def __delitem__(self, i):
        """Delete the entry at index i of the Vector"""
        # If the index is out of range, raise an indexing error
        if not self.index_in_range(i):
            raise IndexError()
        # Otherwise delete the value
        del self.entries[i]

    def index_in_range(self, index):
        return index < len(self) or index > 0

    def max_width(self):
        MAX = -1
        for entry in self.entries:
            width = len(str(entry))
            MAX = max(MAX, width)
        MAX = MAX + 1
        return MAX

    def __str__(self):
        """Create a String representation of this Vector"""
        spacing = self.max_width() + 2
        if spacing <= 6:
            spacing = 6
        spacing = str(spacing)
        s = "["
        # Iterate over all values and add them to the string
        for i in range(len(self)):
            spaced_string = "{:" + spacing + ".2f}"
            s += spaced_string.format(self.entries[i])
            if i < len(self.entries) - 1:
                s += ", "

        s += "]"
        return s

    def __add__(self, vector):
        """Add on a vector to the current vector, and return it as a new instance."""
        # If the other value isn't a vector it can't be added
        if not isinstance(vector, Vector):
            return None

        # If vectors are not of equal length, they can't be added
        if len(self) != len(vector):
            raise ValueError("Cannot add vectors of different lengths.")

        # Create a new list of entries, where each entry is the sum of he
        # individual
        # entries
        entries = []
        for i in range(len(vector)):
            entries.append(self[i] + vector[i])
        # Unpack and convert the list to a vector
        return Vector(entries)

    def __sub__(self, vector):
        """Subtract a vector from the current vector, and return it as a new instance."""
        return self + (vector * -1)

    def cross(self, vector):
        if not isinstance(vector, Vector):
            raise ValueError("Can only compute cross products between vectors")

        if len(self) != 3 and len(vector) != 3:
            raise AssertionError("Can only compute cross products between 3*3 vectors")

        width = len(self)
        cross_matrix = Matrix.Matrix([Vector([1] * width), self, vector])

        i = cross_matrix.copy()
        i.delete_row_vector(0)
        i.delete_column_vector(0)

        j = cross_matrix.copy()
        j.delete_row_vector(0)
        j.delete_column_vector(1)

        k = cross_matrix.copy()
        k.delete_row_vector(0)
        k.delete_column_vector(2)

        return Vector([i.determinant(), -j.determinant(), k.determinant()])

    def dot(self, vector):
        """Find the dot product of one vector with another"""
        # If the value given is a vector, we want to find the dot product of the
        # two
        # vectors
        if isinstance(vector, Vector):
            # Make sure the vectors have the same length
            if len(self) != len(vector):
                raise ValueError("Cannot perform a dot product on Vectors of different length.")
            # The dot product is the sum of all the individual values by each
            # other
            dot = 0
            for i in range(len(vector)):
                dot += self[i] * vector[i]
            # Return the dot
            return dot

    def __mul__(self, value):
        """Find the dot product of one vector with another, or scale the vector by a given value"""
        # If the value given is a vector, we want to find the dot product of the
        # two
        # vectors
        if isinstance(value, Vector):
            return self.dot(value)
        # If the provided value was numerical, we want to scale the vector by
        # the
        # given amount
        elif isinstance(value, float) or isinstance(value, int):
            # Scale each entry and return a new vector of the entries
            values = []
            for i in range(len(self)):
                values.append(self[i] * value)

            # Convert the unpacked list to a vector
            return Vector(values)

    def __lt__(self, other):
        """Check whether one vector is less than the other"""
        # If the other value isn't a vector, it isn't less than this one
        if not isinstance(other, Vector):
            return False
        else:
            # Compare the square Magnitudes, since it is a cheaper calculation
            # than
            # computing the square root
            return self.sqr_magnitude() < other.sqr_magnitude()

    def __gt__(self, other):
        """Check whether one vector is greater than the other"""
        if other == self:
            return False
        else:
            return not self < other

    def __eq__(self, other):
        """Check whether two vectors are equal, they are equal if all entries match"""
        # If the other value isn't a vector, they aren't equal
        if not isinstance(other, Vector):
            return False
        else:
            # Compare the list entries
            return self.entries == other.entries

    def __ne__(self, other):
        """Check whether two vectors are not equal, they are not equal if one of thier entries don't match"""
        return not (self == other)

    def __ge__(self, other):
        """Check whether or not two vectors are greater than or equal to each other"""
        # Make sure we are comparing vectors
        if not isinstance(other, Vector):
            return False
        else:
            # Make the comarison
            return self > other or self == other

    def __le__(self, other):
        """Check whether or not two vectors are less than or equal to each other"""
        # Make sure we are comparing vectors
        if not isinstance(other, Vector):
            return False
        else:
            # Make the comparison
            return self < other or self == other

    def sqr_magnitude(self):
        """Find the square of the magnitude of this vector (faster than finding the magnitude)"""
        # Sum up all the squares of each values
        total = 0
        for value in self.entries:
            total += value * value
        return total

    def magnitude(self):
        """Find the magnitude of this vector"""
        # Return the square root of the square magnitude
        return math.sqrt(self.sqr_magnitude())

    def is_zero(self):
        """Check whether or not this vector is a zero vector"""
        # A zero vector has zero magnitude
        return self.sqr_magnitude() == 0
