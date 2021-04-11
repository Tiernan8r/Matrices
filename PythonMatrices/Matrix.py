from Vector import Vector as Vector


class Matrix(object):
    """A Matrix is effectively a table of values or a list of Vectors"""

    # The rows stores each row of the matrix as a vector
    rows = []

    def __init__(self, rows: list):
        """Create a new Matrix where rows is an arbitrary amount of Vector objects"""

        # If no row vectors were provided stop
        if len(rows) == 0:
            return

        # If the input was a list of Vectors, and only one list was provided
        if len(rows) == 1 and isinstance(rows[0], list):
            # Set the list of row vectors to be the first and only entry in the
            # parent
            # list
            rows = rows[0]

        # Make sure each row is a Vector
        for i in range(len(rows)):
            # Unpack the row into the constructor
            row = rows[i]
            vector = None
            if isinstance(row, list):
                vector = Vector(row)
            elif isinstance(row, Vector):
                vector = row
            rows[i] = vector

        # In order to ensure that the matrix has even dimensions, make sure all
        # vectors have same length
        if len(rows) > 0:
            row_length = len(rows[0])
            for row in rows:
                if len(row) != row_length:
                    raise BaseException("Matrix must have row vectors of equal length.")

        self.rows = rows

    def copy(self):
        new_rows = []
        for row_vector in self.rows:
            new_entries = []
            for entry in row_vector:
                new_entries += [entry]
            new_rows += [Vector(new_entries)]
        return Matrix(new_rows)

    @staticmethod
    def identity(size):
        """Create a square identity matrix of the given dimensions"""

        # Initialise the list of rows to be he desired length
        rows = [[0] * size] * size
        # Iterate over every new row in the matrix
        for i in range(size):
            for j in range(size):
                if i == j:
                    rows[i][j] = 1

        for i in range(size):
            rows[i] = Vector(rows[i])
        return Matrix(rows)

    def row_length(self):
        """Return the amount of horizontal entries in the matrix (assuming symmetry)"""
        return len(self.column_vectors())

    def __len__(self):
        return self.row_length()

    def column_length(self):
        """Return the amount of vertical entries in the matrix (assuming symmetry)"""
        return len(self.row_vectors())

    def is_square(self):
        """A check to see whether the matrix has equal column and row dimensions"""
        return self.row_length() == self.column_length()

    def is_zero(self):
        """A Check to see whether the Matrix has all zero entries"""
        for row in self.row_vectors():
            # If one of the row Vectors isn't zero, the matrix isn't zero
            if not row.is_zero():
                return False
        # Otherwise the matrix is zero
        return True

    def row_vectors(self):
        """Get all the row vectors in the matrix"""
        return self.rows

    def column_vectors(self):
        """Get all the columns vectors in the matrix"""

        # Get the row_vectors and the length of the first row
        # It is assumed that all rows have equal length
        rows = self.row_vectors()
        row_length = len(rows[0])
        # Create an empty list for the column Vectors
        column_vectors = []
        # Iterate over all the indices in the row length
        for i in range(row_length):
            # Create an empty list for the entries in this column vector
            entries = []
            # Iterate over all rows vertically and grab the ith entry in it and add this to the entries list
            for row in rows:
                entries.append(row[i])
            # unpack and convert the list to a vector and add it to the column vectors list
            column = Vector(entries)
            column_vectors.append(column)

        return column_vectors

    def get_row_vector(self, column_index):
        """Get the row vector columnIndex rows from the first row"""
        rows = self.row_vectors()
        # If we only check make sure column index is not out of range and not check whether it is Negative,
        # we can allow for negative indexing
        if column_index > len(rows):
            return None

        return rows[column_index]

    def set_row_vector(self, column_index, vector):
        """Allows you to set the row vector at column index to the vector vector"""
        # Make sure vector is a vector
        if not isinstance(vector, Vector):
            return

        # Make sure column_index is in range
        rows = self.row_vectors()
        if column_index > len(rows):
            return

        # Make sure that the length of vector is the same as the other row
        # vectors:
        if len(vector) != self.row_length():
            return

        # Set the vector
        self.rows[column_index] = vector

    def delete_row_vector(self, column_index):
        """Delete the row vector column_index rows from the first row"""

        # If we only check make sure column index is not out of range and not
        # check
        # whether it is
        # Negative, we can allow for negative indexing
        if column_index > len(self):
            return

        del self.rows[column_index]

    def __getitem__(self, column_index):
        """Equivalent to getRowVector(), but allows for indexing shorthand"""
        return self.get_row_vector(column_index)

    def __setitem__(self, column_index, value):
        """Equivalent to setRowVector(), but allows for indexing shorthand"""
        self.set_row_vector(column_index, value)

    def __delitem__(self, column_index):
        self.delete_row_vector(column_index)

    def get_column_vector(self, row_index):
        """Get the column vector row_index units horizontally from the first column"""
        # Make sure the index is not out of range
        columns = self.column_vectors()
        if row_index > len(columns):
            return None
        # Return the value
        return columns[row_index]

    def set_column_vector(self, row_index, vector):
        """Get the column vector row_index units horizontally from the first column"""
        # Make sure vector is a vector
        if not isinstance(vector, Vector):
            return

        # Make sure row_index is in range
        columns = self.column_vectors()
        if row_index > len(columns):
            return

        # Make sure vector vector has the same length as the column vectors:
        if len(vector) != self.column_length():
            return

        # Get all rows in the matrix
        rows = self.rows
        # Iterate vertically over row indices
        for i in range(self.column_length()):
            # Get the current row
            row = rows[i]
            # Set the vector at row index to be this vertical index vector from
            # vector
            row[row_index] = vector[i]
            # Reassign the row vector in this matrix
            self[i] = row

    def delete_column_vector(self, row_index):
        """Delete the column vector row_index units horizontally from the first column"""
        # Make sure the index is not out of range
        if row_index > self.row_length():
            return

        for rowVector in self.row_vectors():
            del rowVector[row_index]

    def determinant(self):

        if not self.is_square():
            raise ArithmeticError("Cannot compute the determinant of a non-square matrix")

        if self.row_length() == 2 and self.column_length() == 2:

            # Det = ad - bc
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        else:

            det = 0
            for i in range(self.row_length()):
                scalar = self[0][i]

                reduced_matrix = self.copy()
                reduced_matrix.delete_row_vector(0)
                reduced_matrix.delete_column_vector(i)

                det += (-1)**i * scalar * reduced_matrix.determinant()

            return det

    def transpose(self):
        return Matrix(self.column_vectors())

    def cofactor_matrix(self):

        vectors = []
        for i in range(self.column_length()):
            entries = []
            for j in range(self.row_length()):
                cofactor_matrix = self.copy()
                cofactor_matrix.delete_row_vector(i)
                cofactor_matrix.delete_column_vector(j)

                cofactor = cofactor_matrix.determinant()
                cofactor *= (-1)**(i + j)

                entries += [cofactor]

            vectors += [Vector(entries)]

        return Matrix(vectors)

    def adjoint(self):
        return self.cofactor_matrix().transpose()

    def inverse(self):
        """Return the inverse of the matrix"""
        # 1 / det(A) * adj(A)
        det_inverse = 1 / self.determinant()
        return self.adjoint() * det_inverse

    def __str__(self):
        """Get a string representation of this Matrix"""
        # Get every row vector as a string on a unique line and concatenate them all together
        s = ""
        i = 0
        for row_vector in self.rows:
            s += str(row_vector)
            if i < len(self.rows) - 1:
                s += "\n"
            i += 1
        return s

    def __add__(self, matrix):
        """Add the values of the matrix matrix to the values of this matrix"""

        # Make sure that the matrices have equal dimensions
        if self.row_length() != matrix.row_length() or self.column_length() != matrix.column_length():
            raise ValueError("Can only add two Matrices of equal dimensions.")

        # Create a new list to store the row Vectors
        new_rows = []
        # Iterate over all the row vectors indices
        for i in range(self.column_length()):
            # Get the rows for this index form each matrix
            matrix_row1 = self.get_row_vector(i)
            matrix_row2 = matrix.get_row_vector(i)
            # Add the rows and save the value to the list
            new_row_vector = matrix_row1 + matrix_row2
            new_rows.append(new_row_vector)
        # Create a new matrix from the list of values
        return Matrix(new_rows)

    def __sub__(self, matrix):
        """Subtract all the values of the matrix matrix from the values in this matrix"""
        return self + (matrix * -1)

    def __mul__(self, value):
        """Multiply a matrix by another matrix, or scale up the matrix according to a numerical scale"""
        # If the value is numerical we want to scale every value in the matrix
        if isinstance(value, float) or isinstance(value, int):
            # Scale every row in the matrix by the value and return the answer as a new matrix
            rows = []
            for i in range(self.column_length()):
                new_row = self.get_row_vector(i) * value
                rows.append(new_row)

            return Matrix(rows)
        # If the other value is a matrix, we need to multiply the two matrices
        # together
        elif isinstance(value, Matrix):
            # Make sure the length of the rows for one matrix matches the column
            # length
            # of the other,
            # Otherwise we can't comput the multiplication
            if self.row_length() != value.column_length():
                return None

            # Get the rows from the first matrix
            matrix1_rows = self.row_vectors()
            # Get the columns from the other matrix
            matrix2_columns = value.column_vectors()
            # Save the vector of dot products of each row and column in this
            # array
            product_rows = []

            # Iterate over every row in the first matrix
            for row in matrix1_rows:

                # Find the dot product of this row with every column in the
                # other matrix
                entries = []
                for column in matrix2_columns:
                    product = row * column
                    # Save the answer in the entries list for this row vector
                    entries.append(product)
                # Unpack and convert the list to a vector
                new_row = Vector(entries)
                # Add the vector to the list of row vector
                product_rows.append(new_row)
            # Convert the list of rows to a matrix and return it
            return Matrix(product_rows)

    def __pow__(self, power):
        """Compute the value of the matrix raised to the power of power"""
        # The powering computation uses binary powering for speed and efficiency

        # If the power is zero, we want the identity matrix
        if power == 0:
            # We can only get the identity matrix if the matrix is square,
            # otherwise we
            # get an invalid value
            if not self.is_square():
                return None
            # Return the identity matrix for this value
            return Matrix.identity(self.row_length())

        # If the power is 1, the matrix doesn't change
        if power == 1:
            return self

        # If the power is negative, we find the inverse of the matrix to the
        # power as
        # a positive
        if power < 0:
            return (self.inverse())**-power

        # If the power is even, multiply the matrix by itself and by the matrix
        # to the
        # half power less 1
        if power % 2 == 0:
            return (self * self)**(power // 2)
        # Otherwise multiply the matrix by itself to the power less 1
        else:
            return self * (self**(power - 1))
