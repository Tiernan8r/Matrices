using System;
using System.Collections.Generic;

namespace Matrices {

	class Vector {

		private readonly List<float> values;

		public Vector(params float[] entries) {
			List<float> asList = new List<float>();
			foreach(float entry in entries) {
				asList.Add(entry);
			}

			values = asList;
		}

		public Vector(List<float> values) {
			this.values = values;
		}

		public Vector Copy() {
			List<float> newValues = new List<float>(values);
			return new Vector(newValues);
		}

		public int Length => values.Count;

		private bool IndexInRange(int index) {
			return index > 0 || index < Length;
		}

		public List<float> GetEntries() {
			return values;
		}

		public float Get(int i) {

			if(!IndexInRange(i)) {
				throw new IndexOutOfRangeException();
			}

			return values[i];

		}

		public void Set(int i, float value) {

			if(!IndexInRange(i)) {
				throw new IndexOutOfRangeException();
			}

			values[i] = value;
		}

		public void Delete(int i) {
			if(!IndexInRange(i)) {
				throw new IndexOutOfRangeException();
			}

			values.RemoveAt(i);
		}

		public float this[int i] {
			get => Get(i);
			set => Set(i, value);
		}

		public override string ToString() {
			string s = "[";
			for(int i = 0; i < Length; i++) {
				float value = Get(i);
				s += value;
				if(i < Length - 1) {
					s += ", ";
				}
			}

			s += "]";
			return s;
		}

		public static Vector operator +(Vector vector1, Vector vector2) {

			if(vector1.Length != vector2.Length) {
				throw new ArgumentException("Cannot add vectors of different lengths.");
			}

			for(int i = 0; i < vector1.Length; i++) {
				vector1[i] += vector2[i];
			}

			return vector1;

		}

		public static Vector operator -(Vector vector1, Vector vector2) {

			return vector1 + (vector2 * -1);

		}

		public Vector Cross(Vector vector) {

			if(Length != 3 && vector.Length != 3) {
				throw new ArithmeticException("Can only compute cross products between 3*3 vectors");
			}

			Matrix crossMatrix = new Matrix(new Vector(1, 1, 1), this, vector);

			Matrix i = crossMatrix.Copy();
			i.DeleteRowVector(0);
			i.DeleteColumnVector(0);

			Matrix j = crossMatrix.Copy();
			j.DeleteRowVector(0);
			j.DeleteColumnVector(1);

			Matrix k = crossMatrix.Copy();
			k.DeleteRowVector(0);
			k.DeleteColumnVector(2);

			return new Vector(i.Determinant(), -j.Determinant(), k.Determinant());

		}

		public float Dot(Vector vector) {

			if(Length != vector.Length) {
				throw new ArgumentException("Cannot perform a dot product on Vectors of different length.");
			}

			float dot = 0;
			for(int i = 0; i < Length; i++) {
				dot += this[i] * vector[i];
			}

			return dot;

		}

		public static float operator *(Vector vector1, Vector vector2) {

			return vector1.Dot(vector2);

		}

		public static Vector operator *(Vector vector, float scalar) {

			for(int i = 0; i < vector.Length; i++) {
				vector[i] *= scalar;
			}

			return vector;

		}

		public static bool operator <(Vector vector1, Vector vector2) {
			return vector1.SqrMagnitude() < vector2.SqrMagnitude();
		}

		public static bool operator >(Vector vector1, Vector vector2) {
			return vector1.SqrMagnitude() > vector2.SqrMagnitude();
		}

		public static bool operator ==(Vector vector1, Vector vector2) {

			if(vector1 is null || vector2 is null) {
				if(vector1 is null && vector2 is null) {
					return true;
				}

				return false;
			}

			return vector1.Equals(vector2);

		}

		public override bool Equals(object obj) {

			if(!(obj is Vector)) {
				return false;
			}

			Vector vector = (Vector) obj;

			if(Length != vector.Length) {
				return false;
			}

			bool equals = true;
			for(int i = 0; i < Length; i++) {
				if(!equals) {
					break;
				}

				equals = this[i] == vector[i];
			}

			return equals;
		}

		public static bool operator >=(Vector vector1, Vector vector2) {
			return vector1 > vector2 || vector1 == vector2;
		}

		public static bool operator <=(Vector vector1, Vector vector2) {
			return vector1 < vector2 || vector1 == vector2;
		}

		public static bool operator !=(Vector vector1, Vector vector2) {
			return !(vector1 == vector2);
		}

		public override int GetHashCode() {
			int hashCode = 515162400;
			hashCode = hashCode * -1521134295 + EqualityComparer<float[]>.Default.GetHashCode(values.ToArray());
			hashCode = hashCode * -1521134295 + Length.GetHashCode();
			return hashCode;
		}

		public float SqrMagnitude() {
			float sum = 0;
			foreach(float entry in values) {
				sum += entry * entry;
			}

			return sum;
		}

		public float Magnitude() {
			return (float) Math.Sqrt(SqrMagnitude());
		}

		public bool IsZero() {
			return SqrMagnitude() == 0;
		}

	}

}