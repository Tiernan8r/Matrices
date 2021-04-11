using Matrices;
using System;
using System.Collections.Generic;

class Program {

	static void Main(string[] args) {

		//Vector[] vectors = new Vector[] {
		//		new Vector(1, 2, 3),
		//		new Vector(0, 4, 5),
		//		new Vector(1, 0, 6),
		//	};

		//Matrix A = new Matrix(vectors);

		//Console.WriteLine(A);
		//Console.WriteLine("Is Square? " + A.IsSquare);

		//Console.WriteLine();

		////Matrix B = ReadMatrix();

		//Matrix cofactor = A.Cofactor();
		//Console.WriteLine(cofactor);
		//Console.WriteLine();

		//Matrix adjoint = A.Adjoint();
		//Console.WriteLine(adjoint);
		//Console.WriteLine();

		//float determinant = A.Determinant();
		//Console.WriteLine(determinant);
		//Console.WriteLine();

		//Matrix inverse = A.Inverse();
		//Console.WriteLine(inverse);

		//Console.WriteLine();
		//Console.WriteLine(A + B);

		//Console.WriteLine();
		//Console.WriteLine(A - B);

		//Console.WriteLine();
		//Console.WriteLine(A * B);

		//Console.Write("B^Power: Power = ?: ");
		//int power = int.Parse(Console.ReadLine());

		//Console.WriteLine();
		//Console.WriteLine(B^power);

		Console.WriteLine("Give values for A:");
		Matrix A = ReadMatrix();

		Console.WriteLine("\nGive values for C:");
		Matrix C = ReadMatrix();

		Console.WriteLine("\nGive values for R:");
		Vector R = ReadVector();
		Console.WriteLine("\nGive values for F:");
		Vector F = ReadVector();

		bool safe = SafeState(C, A, R, F);
		Console.WriteLine("Is Safe State? " + safe);

#if DEBUG
		Console.WriteLine("Press Enter to quit:");
		Console.ReadLine();
#endif

	}

	private static Matrix ReadMatrix() {

		List<Vector> rowVectors = new List<Vector>();

		while(true) {

			Console.WriteLine();
			Vector vector = ReadVector();

			if(vector == null) {
				break;
			} else {
				rowVectors.Add(vector);
			}

		}

		if(rowVectors.Count == 0) {
			return null;
		} else {
			return new Matrix(rowVectors.ToArray());
		}

	}

	private static Vector ReadVector() {

		List<float> entries = new List<float>();

		Console.Write("Enter the values for the vector, seperated by a ',': ");
		string input = Console.ReadLine();

		string[] values = input.Split(',');

		foreach(string number in values) {

			float entry = 0;
			try {
				entry = float.Parse(number);
			} catch {
				Console.WriteLine(number + " is not a valid number, ignoring it.");
				continue;
			}
			entries.Add(entry);

		}

		if(entries.Count == 0) {
			return null;
		} else {
			return new Vector(entries.ToArray());
		}

	}

	private static bool SafeState(Matrix C, Matrix A, Vector R, Vector F) {

		Matrix N = C - A;

		Console.WriteLine(N);

		int i = 0;
		int skips = 0;

		while(!N.IsZero() && skips < N.ColumnLength - 1) {

			Vector process = N[i];
			Console.WriteLine("Process " + i + " = " + process);

			if(process.SqrMagnitude() < F.SqrMagnitude() && !process.IsZero()) {

				F += process;
				for(int j = 0; j < process.Length; j++) {
					process[j] = 0;
				}
				Console.WriteLine(process);

				C[i] = process;
				A[i] = process;
				N[i] = process;

				Console.WriteLine("Execute Process " + i);

			} else {
				skips++;
			}

			i++;

			if(i >= N.ColumnLength - 1) {
				i = 0;
				skips = 0;
			}

		}
		Console.WriteLine(N);
		Console.WriteLine("Skips: " + skips + " < " + N.ColumnLength + "?");

		return N.IsZero();

	}

}

