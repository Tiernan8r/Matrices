package me.Tiernan.Matrices;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Vector {

	private List<Float> values;

	public Vector(float[] values) {
		List<Float> asList = new LinkedList<Float>();
		for (float entry : values) {
			asList.add(entry);
		}
		this.values = asList;
	}

	public Vector(List<Float> values) {
		this.values = values;
	}

	public Vector copy() {
		List<Float> newEntries = new LinkedList<>(getEntries());
		return new Vector(newEntries);
	}

	public int getLength() {
		return this.values.size();
	}

	private boolean indexInRange(int index) {
		return index > 0 || index < getLength();
	}

	public List<Float> getEntries() {
		return this.values;
	}

	public float get(int i) {

		if (!indexInRange(i)) {
			throw new IndexOutOfBoundsException();
		}

		return this.getEntries().get(i);

	}

	public void set(int i, float value) {
		if (!indexInRange(i)) {
			throw new IndexOutOfBoundsException();
		}
		this.values.set(i, value);
	}

	public void delete(int i) {
		if (!indexInRange(i)) {
			throw new IndexOutOfBoundsException();
		}

		List<Float> entries = this.getEntries();
		entries.remove(i);
		this.values = entries;

	}

	public String toString() {

		String s = "[";
		List<Float> entries = this.getEntries();
		for (int i = 0; i < getLength(); i++) {

			float value = entries.get(i);
			s += value;

			if (i < getLength() - 1) {
				s += ", ";
			}

		}
		s += "]";

		return s;

	}

	public Vector add(Vector vector) {

		if (getLength() != vector.getLength()) {
			try {
				throw new Exception("Cannot add vectors of different lengths.");
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		float[] entries = new float[getLength()];

		for (int i = 0; i < getLength(); i++) {
			entries[i] = get(i) + vector.get(i);
		}

		return new Vector(entries);

	}

	public Vector subtract(Vector vector) {
		return this.add(vector.scale(-1));
	}

	public Vector cross(Vector vector) {

		if (this.getLength() != 3 && vector.getLength() != 3) {
			throw new ArithmeticException("Can only compute cross products between 3*3 vectors");
		}

		Vector firstRow = new Vector(new float[]{1, 1, 1});
		Matrix crossMatrix = new Matrix(new Vector[]{firstRow, this, vector});

		Matrix i = crossMatrix.copy();
		i.deleteRowVector(0);
		i.deleteColumnVector(0);

		Matrix j = crossMatrix.copy();
		j.deleteRowVector(0);
		j.deleteColumnVector(1);

		Matrix k = crossMatrix.copy();
		k.deleteRowVector(0);
		k.deleteColumnVector(2);

		List<Float> entries = new ArrayList<>();
		entries.add(i.determinant());
		entries.add(-j.determinant());
		entries.add(k.determinant());

		return new Vector(entries);
	}

	public float dot(Vector vector) {

		if (getLength() != vector.getLength()) {
			throw new ArithmeticException("Cannot perform a dot product on Vectors of different length.");
		}

		float dot = 0;
		List<Float> entries = getEntries();
		List<Float> vectorEntries = vector.getEntries();
		for (int i = 0; i < getLength(); i++) {
			dot += entries.get(i) * vectorEntries.get(i);
		}
		return dot;

	}

	public Vector scale(float scalar) {

		List<Float> entries = getEntries();
		for (int i = 0; i < entries.size(); i++) {
			float value = entries.get(i) * scalar;
			entries.set(i, value);
		}

		this.values = entries;
		return this;

	}

	public boolean lessThan(Vector vector) {
		// Compare the square Magnitudes, since it is a cheaper calculation than computing the square root
		return this.sqrMagnitude() < vector.sqrMagnitude();
	}

	public boolean greaterThan(Vector vector) {
		if (vector.equals(this)) {
			return false;
		} else {
			return !(this.lessThan(vector));
		}
	}

	public boolean equals(Vector vector) {
		// Compare the list entries
		return getEntries().equals(vector.getEntries());
	}

	public boolean greaterEqual(Vector vector) {
		return this.greaterThan(vector) || this.equals(vector);
	}

	public boolean lesserEqual(Vector vector) {
		return this.lessThan(vector) || this.equals(vector);
	}

	public float sqrMagnitude() {
		// Sum up all the squares of each values
		float total = 0;
		for (float value : getEntries()) {
			total += value * value;
		}
		return total;
	}

	public float magnitude() {
		//Return the square root of the square magnitude
		return (float) Math.sqrt(sqrMagnitude());
	}

	public boolean isZero() {
		float epsilon = 0.001f;
		//A zero vector has zero magnitude
		return sqrMagnitude() <= epsilon;
	}

}
