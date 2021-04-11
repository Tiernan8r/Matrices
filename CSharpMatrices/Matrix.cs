using System;
using System.Collections.Generic;

namespace Matrices {

	class Matrix {

		private readonly List<Vector> rows;

		public Matrix(params Vector[] rows) {
			List<Vector> vectors = new List<Vector>();
			foreach(Vector vector in rows) {
				vectors.Add(vector);
			}

			this.rows = vectors;
		}

		public Matrix(List<Vector> rows) {
			this.rows = rows;
		}

		public static Matrix Identity(int size) {
			List<Vector> rows = new List<Vector>();
			for(int i = 0; i < size; i++) {
				List<float> entries = new List<float>();
				for(int j = 0; j < size; j++) {
					entries.Add(i == j ? 1f : 0f);
				}

				Vector row = new Vector(entries);
				rows.Add(row);
			}

			return new Matrix(rows);
		}

		public Matrix Copy() {

			List<Vector> newVectors = new List<Vector>();
			foreach(Vector vector in RowVectors()) {
				Vector newVector = vector.Copy();
				newVectors.Add(newVector);
			}

			return new Matrix(newVectors);
		}

		private bool RowIndexInRange(int index) {
			return index < RowLength || index > 0;
		}

		private bool ColumnIndexInRange(int index) {
			return index < ColumnLength || index > 0;
		}

		public int RowLength => ColumnVectors().Count;

		public int ColumnLength => RowVectors().Count;

		public bool IsSquare => RowLength == ColumnLength;

		public bool IsZero() {
			foreach(Vector row in RowVectors()) {
				if(!row.IsZero())
					return false;
			}

			return true;

		}

		public List<Vector> RowVectors() {
			return rows;
		}

		public List<Vector> ColumnVectors() {

			List<Vector> rowVectors = RowVectors();
			int rowLength = rowVectors[0].Length;
			List<Vector> columnVectors = new List<Vector>();
			for(int i = 0; i < rowLength; i++) {
				List<float> entries = new List<float>();
				foreach(Vector row in rowVectors) {
					entries.Add(row[i]);
				}

				Vector column = new Vector(entries);
				columnVectors.Add(column);
			}

			return columnVectors;

		}

		public Vector GetRowVector(int columnIndex) {

			if(!ColumnIndexInRange(columnIndex)) {
				throw new IndexOutOfRangeException();
			}

			return rows[columnIndex];

		}

		public void SetRowVector(int columnIndex, Vector vector) {
			//Make sure value is a vector

			// Make sure columnIndex is in range
			if(!ColumnIndexInRange(columnIndex)) {
				return;
			}

			// Make sure that the length of value is the same as the other row
			//vectors:
			if(vector.Length != RowLength) {
				return;
			}

			// Set the value
			rows[columnIndex] = vector;
		}

		public void DeleteRowVector(int columnIndex) {

			if(!ColumnIndexInRange(columnIndex)) {
				throw new IndexOutOfRangeException();
			}

			rows.RemoveAt(columnIndex);

		}

		public Vector GetColumnVector(int rowIndex) {

			if(!RowIndexInRange(rowIndex)) {
				throw new IndexOutOfRangeException();
			}

			List<Vector> columns = ColumnVectors();

			return columns[rowIndex];


		}

		public void SetColumnVector(int rowIndex, Vector value) {

			//Make sure rowIndex is in range
			if(!RowIndexInRange(rowIndex)) {
				return;
			}

			//Make sure value vector has the same length as the column vectors:
			if(value.Length != ColumnLength) {
				return;
			}

			//Iterate vertically over row indices
			for(int i = 0; i < ColumnLength; i++) {
				//Get the current row
				Vector row = GetRowVector(i);
				// Set the value at row index to be this vertical index value from
				// value
				row[rowIndex] = value[i];
				//Reassign the row vector in this matrix
				this[i] = row;
			}
		}

		public void DeleteColumnVector(int rowIndex) {

			if(!RowIndexInRange(rowIndex)) {
				throw new IndexOutOfRangeException();
			}

			foreach(Vector row in rows) {
				row.Delete(rowIndex);
			}

		}

		public float Determinant() {

			if(!IsSquare) {
				throw new ArithmeticException("Cannot compute the determinant of a non-square matrix");
			}

			if(RowLength == 2 && ColumnLength == 2) {
				//Det = ad - bc
				return this[0][0] * this[1][1] - this[0][1] * this[1][0];
			}
			else {

				float det = 0;
				for(int i = 0; i < RowLength; i++) {
					float scalar = this[0][i];

					Matrix reducedMatrix = Copy();
					reducedMatrix.DeleteRowVector(0);
					reducedMatrix.DeleteColumnVector(i);

					det += ((-1) ^ i) * scalar * reducedMatrix.Determinant();
				}

				return det;
			}
		}

		public Matrix Transpose() => new Matrix(ColumnVectors());

		public Matrix Cofactor() {

			List<Vector> vectors = new List<Vector>();
			for(int i = 0; i < ColumnLength; i++) {

				List<float> entries = new List<float>();

				for(int j = 0; j < RowLength; j++) {

					Matrix cofactorMatrix = Copy();
					cofactorMatrix.DeleteRowVector(i);
					cofactorMatrix.DeleteColumnVector(j);

					float cofactor = cofactorMatrix.Determinant();
					cofactor *= ((-1) ^ (i + j));

					entries.Add(cofactor);
				}

				vectors.Add(new Vector(entries));
			}

			return new Matrix(vectors);

		}

		public Matrix Adjoint() => Cofactor().Transpose();

		public Matrix Inverse() => Adjoint() * (1 / Determinant());

		public override string ToString() {

			string s = "";
			for(int i = 0; i < RowLength; i++) {

				Vector rowVector = rows[i];
				s += rowVector.ToString();

				if(i < RowLength - 1) {
					s += "\n";
				}

			}

			return s;

		}

		public Vector this[int i] {
			get => GetRowVector(i);
			set => SetRowVector(i, value);
		}

		public static Matrix operator +(Matrix matrix1, Matrix matrix2) {

			if(matrix1.RowLength != matrix2.RowLength && matrix1.ColumnLength != matrix2.ColumnLength) {
				throw new ArgumentException("Can only add two Matrices of equal dimensions.");
			}

			List<Vector> newRows = new List<Vector>();

			for(int i = 0; i < matrix1.ColumnLength; i++) {

				Vector matrixRow1 = matrix1.GetRowVector(i);
				Vector matrixRow2 = matrix2.GetRowVector(i);

				newRows.Add(matrixRow1 + matrixRow2);

			}

			return new Matrix(newRows);
		}

		public static Matrix operator -(Matrix matrix1, Matrix matrix2) {

			return matrix1 + (matrix2 * -1);

		}

		public static Matrix operator *(Matrix matrix, float scalar) {
			List<Vector> rows = new List<Vector>();
			for(int i = 0; i < matrix.ColumnLength; i++) {
				Vector newRow = matrix[i] * scalar;
				rows.Add(newRow);
			}

			return new Matrix(rows);
		}

		public static Matrix operator *(Matrix matrix1, Matrix matrix2) {

			if(matrix1.RowLength != matrix2.ColumnLength) {
				return null;
			}

			List<Vector> matrix1Rows = matrix1.RowVectors();
			List<Vector> matrix2Columns = matrix2.ColumnVectors();

			List<Vector> productRows = new List<Vector>();

			foreach(Vector row in matrix1Rows) {
				List<float> entries = new List<float>();
				foreach(Vector column in matrix2Columns) {
					entries.Add(row * column);
				}

				Vector newRow = new Vector(entries);
				productRows.Add(newRow);
			}

			return new Matrix(productRows);
		}

		public static Matrix operator ^(Matrix matrix, int power) {

			if(power == 0) {
				if(!matrix.IsSquare) {
					return null;
				}

				return Identity(matrix.RowLength);
			}

			if(power == 1) {
				return matrix;
			}

			if(power < 0) {
				return matrix.Inverse() ^ power;
			}

			if(power % 2 == 0) {
				return (matrix * matrix) ^ (power / 2);
			}
			else {

				return matrix * (matrix ^ (power - 1));
			}

		}

	}


}