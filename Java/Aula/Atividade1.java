import java.util.Scanner;
import java.util.Random;

public class Atividade1 {
    
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		Random rd = new Random();

		System.out.println("   LISTA DE EXERCÍCIOS: VETORES E MATRIZES\n   ");

		// Execução sequencia
		ex01_MediaVetor(sc);
		ex02_ContarOcorrencias();
		ex03_IntercalarVetores(sc);
		ex04_InverterVetor();
		ex05_ContagemFaixas(sc);
		ex06_SomaLinhasMatriz(sc);
		ex07_SomaDuasMatrizes(rd);
		ex08_MultiplicacaoMatrizes(rd);

		System.out.println("\nFim. Feito por Lucas Fernandes 10419400");

		sc.close();
	}

	// --- 1: Maiores que a média ---
	public static void ex01_MediaVetor(Scanner sc) {
		System.out.println("\n[EX 01] Elementos maiores que a média");
		System.out.print("Tamanho do vetor (N <= 30): ");
		int n = sc.nextInt();
		int[] vet = new int[n];
		double soma = 0;

		for (int i = 0; i < n; i++) {
			System.out.print("Vetor[" + i + "]: ");
			vet[i] = sc.nextInt();
			soma += vet[i];
		}

		double media = soma / n;
		int cont = 0;
		for (int x : vet)
			if (x > media)
				cont++;

		System.out.println("Média: " + media + " | Maiores que a média: " + cont + "\n");
	}

	// --- 2: Contar elemento X ---
	public static void ex02_ContarOcorrencias() {
		System.out.println("[EX 02] Contar ocorrências de X");
		int[] A = { 10, 5, 8, 10, 3, 10, 2 };
		int x = 10;
		int cont = 0;
		for (int val : A)
			if (val == x)
				cont++;
		System.out.println("Vetor: [10, 5, 8, 10, 3, 10, 2]");
		System.out.println("O número " + x + " aparece " + cont + " vezes.\n");
	}

	// --- 3: Intercalar 2 vetores ---
	public static void ex03_IntercalarVetores(Scanner sc) {
		System.out.println("[EX 03] Intercalar dois vetores de 5 elementos");
		int[] v1 = new int[5];
		int[] v2 = new int[5];
		int[] res = new int[10];

		for (int i = 0; i < 5; i++) {
			System.out.print("Vetor 1 [" + i + "]: ");
			v1[i] = sc.nextInt();
			System.out.print("Vetor 2 [" + i + "]: ");
			v2[i] = sc.nextInt();
			res[2 * i] = v1[i];
			res[2 * i + 1] = v2[i];
		}
		System.out.print("Resultado intercalado: ");
		for (int val : res)
			System.out.print(val + " ");
		System.out.println("\n");
	}

	// --- 4: Inverter vetor ---
	public static void ex04_InverterVetor() {
		System.out.println("[EX 04] Inverter vetor [1, 3, 6, 4, 5, 9]");
		int[] a = { 1, 3, 6, 4, 5, 9 };
		int n = a.length;
		for (int i = 0; i < n / 2; i++) {
			int temp = a[i];
			a[i] = a[n - 1 - i];
			a[n - 1 - i] = temp;
		}
		System.out.print("Saída: ");
		for (int val : a)
			System.out.print(val + " ");
		System.out.println("\n");
	}

	// --- 5: Histograma (Faixas) ---
	public static void ex05_ContagemFaixas(Scanner sc) {
		System.out.println("[EX 05] Contagem por faixas (0-99)");
		System.out.print("Quantos números na sequência? ");
		int n = sc.nextInt();
		int[] faixas = new int[10];
		for (int i = 0; i < n; i++) {
			System.out.print("Digite um número (0-99): ");
			int num = sc.nextInt();
			if (num >= 0 && num <= 99)
				faixas[num / 10]++;
		}
		for (int i = 0; i < 10; i++) {
			System.out.printf("Faixa %02d-%02d: %d ocorrência(s)\n", (i * 10), (i * 10 + 9), faixas[i]);
		}
		System.out.println();
	}

	// --- 6: Soma linhas matriz 3x3 ---
	public static void ex06_SomaLinhasMatriz(Scanner sc) {
		System.out.println("[EX 06] Soma das linhas da matriz 3x3");
		int[][] mat = new int[3][3];
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				System.out.print("Matriz [" + i + "][" + j + "]: ");
				mat[i][j] = sc.nextInt();
			}
		}
		for (int i = 0; i < 3; i++) {
			int soma = 0;
			for (int j = 0; j < 3; j++)
				soma += mat[i][j];
			System.out.println("Soma Linha " + i + ": " + soma);
		}
		System.out.println();
	}

	// --- 7: Soma de Matrizes A + B ---
	public static void ex07_SomaDuasMatrizes(Random rd) {
		System.out.println("[EX 07] Soma de Matrizes A + B (2x4)");
		int[][] A = new int[2][4], B = new int[2][4], C = new int[2][4];
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 4; j++) {
				A[i][j] = rd.nextInt(10);
				B[i][j] = rd.nextInt(10);
				C[i][j] = A[i][j] + B[i][j];
			}
		}
		System.out.println("Matriz Resultante:");
		imprimir(C);
	}

	// --- 8: Multiplicação A x B ---
	public static void ex08_MultiplicacaoMatrizes(Random rd) {
		System.out.println("\n[EX 08] Multiplicação de Matrizes A(2x4) x B(4x2)");
		int[][] A = new int[2][4], B = new int[4][2], C = new int[2][2];
		for (int i = 0; i < 2; i++)
			for (int j = 0; j < 4; j++)
				A[i][j] = rd.nextInt(5);
		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 2; j++)
				B[i][j] = rd.nextInt(5);

		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 2; j++) {
				for (int k = 0; k < 4; k++) {
					C[i][j] += A[i][k] * B[k][j];
				}
			}
		}
		System.out.println("Resultado da Multiplicação:");
		imprimir(C);
	}

	// Auxiliar para imprimir matrizes
	public static void imprimir(int[][] mat) {
		for (int[] linha : mat) {
			for (int val : linha)
				System.out.print(val + "\t");
			System.out.println();
		}
}
    
}
