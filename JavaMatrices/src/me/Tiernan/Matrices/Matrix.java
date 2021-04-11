package me.Tiernan.Matrices;

import java.util.LinkedList;
import java.util.List;

public class Matrix {

	private List<Vector> rows;

	public Matrix(Vector[] vectors) {
		List<Vector> rows = new LinkedList<>();
		for (Vector vector : vectors) {
			rows.add(vector);
		}
		this.rows = rows;
	}

	public Matrix(List<Vector> rows) {
		this.rows = rows;
	}

	public static Matrix identity(int size) {

		List<Vector> rows = new LinkedList<>();

		for (int i = 0; i < size; i++) {

			List<Float> entries = new LinkedList<>();

			for (int j = 0; j < size; j++) {
				entries.add(i == j ? 1f : 0f);
			}

			Vector row = new Vector(entries);
			rows.add(row);

		}

		return new Matrix(rows);

	}

	public Matrix copy() {

		List<Vector> newVectors = new LinkedList<>();
		for (Vector vector : getRowVectors()) {
			Vector newVector = vector.copy();
			newVectors.add(newVector);
		}

		return new Matrix(newVectors);

	}

	private boolean rowIndexInRange(int index) {
		return index < rowLength() || index > 0;
	}

	private boolean columnIndexInRange(int index) {
		return index < columnLength() || index > 0;
	}

	public int rowLength() {
		return getRowVectors().get(0).getLength();
	}

	public int columnLength() {
		return getRowVectors().size();
	}

	public boolean isSquare() {
		return rowLength() == columnLength();
	}

	public boolean isZero() {
		for (Vector row : getRowVectors()) {
			if (!row.isZero()) {
				return false;
			}
		}
		return true;
	}

	public List<Vector> getRowVectors() {
		return this.rows;
	}

	private void setRowVectors(List<Vector> rowVectors) {
		this.rows = rowVectors;
	}

	public List<Vector> getColumnVectors() {

		List<Vector> rows = getRowVectors();
		List<Vector> columnVectors = new LinkedList<>();
		for (int i = 0; i < rowLength(); i++) {
			List<Float> entries = new LinkedList<>();
			for (Vector row : rows) {
				entries.add(row.get(i));
			}
			Vector column = new Vector(entries);
			columnVectors.add(column);
		}

		return columnVectors;

	}

	public Vector getRowVector(int columnIndex) {

		List<Vector> rows = getRowVectors();

		if (!columnIndexInRange(columnIndex)) {
			return null;
		}

		return rows.get(columnIndex);

	}

	public void setRowVector(int columnIndex, Vector vector) {
		if (!columnIndexInRange(columnIndex)) {
			return;
		}
		List<Vector> rowVectors = getRowVectors();
		rowVectors.set(columnIndex, vector);
		setRowVectors(rowVectors);

	}

	public void deleteRowVector(int columnIndex) {

		if (!columnIndexInRange(columnIndex)) {
			return;
		}
		List<Vector> rowVectors = getRowVectors();
		rowVectors.remove(columnIndex);
		setRowVectors(rowVectors);

	}

	public Vector getColumnVector(int rowIndex) {
		if (!rowIndexInRange(rowIndex)) {
			return null;
		}
		List<Vector> columns = getColumnVectors();
		return columns.get(rowIndex);
	}

	public void setColumnVector(int rowIndex, Vector vector) {
		if (!columnIndexInRange(rowIndex)) {
			return;
		}

		List<Vector> rowVectors = getRowVectors();
		for (int i = 0; i < rowVectors.size(); i++) {
			Vector row = rowVectors.get(i);
			row.set(rowIndex, vector.get(i));
		}
		setRowVectors(rowVectors);

	}

	public void deleteColumnVector(int rowIndex) {
		if (!columnIndexInRange(rowIndex)) {
			return;
		}

		List<Vector> rowVectors = getRowVectors();
		for (Vector row : rowVectors) {
			row.delete(rowIndex);
		}
		setRowVectors(rowVectors);
	}

	public float determinant() {

		if (isSquare()) {
			throw new ArithmeticException("Cannot compute the determinant of a non-square matrix");
		}

		if (rowLength() == 2 && columnLength() == 2) {
			//Det = ad - bc
			List<Vector> rowVectors = getRowVectors();
			float a = rowVectors.get(0).get(0);
			float b = rowVectors.get(0).get(1);
			float c = rowVectors.get(1).get(0);
			float d = rowVectors.get(1).get(1);
			return a * d - b * c;
		} else {

			float determinant = 0;
			for (int i = 0; i < rowLength(); i++) {
				float scalar = getRowVector(0).get(i);
				Matrix reducedMatrix = this.copy();
				reducedMatrix.deleteRowVector(0);
				reducedMatrix.deleteColumnVector(i);
				float pow = (float) Math.pow(-1, i);
				determinant += pow * scalar * reducedMatrix.determinant();
			}
			return determinant;
		}

	}

	public Matrix transpose() {
		return new Matrix(getColumnVectors());
	}

	public Matrix cofactorMatrix() {

		List<Vector> vectors = new LinkedList<>();
		for (int i = 0; i < columnLength(); i++) {
			List<Float> entries = new LinkedList<>();
			for (int j = 0; j < rowLength(); j++) {
				Matrix cofactorMatrix = copy();
				cofactorMatrix.deleteRowVector(i);
				cofactorMatrix.deleteColumnVector(j);

				float cofactor = cofactorMatrix.determinant();
				cofactor *= Math.pow(-1, i + j);
				entries.add(cofactor);
			}
			vectors.add(new Vector(entries));
		}
		return new Matrix(vectors);
	}

	public Matrix adjoint() {
		return cofactorMatrix().transpose();
	}

	public Matrix inverse() {
		// 1 / det(A) * adj(A)
		float detInverse = 1 / determinant();
		return adjoint().scale(detInverse);
	}

	public String toString() {
		String s = "";
		for (int i = 0; i < rowLength(); i++) {
			Vector rowVector = getRowVector(i);
			s += rowVector.toString();
			if (i < rowLength() - 1) {
				s += "\n";
			}
		}
		return s;
	}

	public Matrix add(Matrix matrix) {

		if (rowLength() != matrix.rowLength() && columnLength() != matrix.columnLength()) {
			throw new ArithmeticException("Can only add two Matrices of equal dimensions.");
		}

		List<Vector> newRows = new LinkedList<>();
		for (int i = 0; i < columnLength(); i++) {
			Vector matrixRow1 = getRowVector(i);
			Vector matrixRow2 = matrix.getRowVector(i);

			Vector newRowVector = matrixRow1.add(matrixRow2);
			newRows.add(newRowVector);
		}
		return new Matrix(newRows);
	}

	public Matrix subtract(Matrix matrix) {
		Matrix negative = matrix.scale(-1f);
		return this.add(negative);
	}

	public Matrix scale(float scalar) {
		List<Vector> rows = new LinkedList<>();
		for (int i = 0; i < columnLength(); i++) {
			Vector newRow = getRowVector(i).scale(scalar);
			rows.add(newRow);
		}
		return new Matrix(rows);
	}

	public Matrix multiply(Matrix matrix) {
		if (rowLength() != matrix.columnLength()) {
			return null;
		}
		List<Vector> matrix1Rows = getRowVectors();
		List<Vector> matrix2Columns = matrix.getColumnVectors();

		List<Vector> productRows = new LinkedList<>();

		for (Vector row : matrix1Rows) {

			List<Float> entries = new LinkedList<>();
			for (Vector column : matrix2Columns) {
				float product = row.dot(column);
				entries.add(product);
			}
			productRows.add(new Vector(entries));
		}
		return new Matrix(productRows);
	}

	public Matrix power(int power) {
		if (power == 0) {
			if (!isSquare()) {
				return null;
			}
			return Matrix.identity(rowLength());
		}

		if (power == 1) {
			return this;
		}

		if (power < 0) {
			return (this.inverse()).power(-power);
		}

		if (power % 2 == 0) {
			return this.multiply(this).multiply(this.power(((power / 2) - 1)));
		} else {
			return this.multiply(this.power((power - 1)));
		}

	}

}
