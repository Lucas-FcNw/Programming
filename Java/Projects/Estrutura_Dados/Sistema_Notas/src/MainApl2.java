
import apl2.DLinkedList;
import apl2.LinkedListOriginal;
import apl2.Operation;
import apl2.Data;

public class MainApl2 {

    public static void main(String[] args) {
        LinkedListOriginal list = new LinkedListOriginal();

        try {
            String dados = Data.loadTextFileToString("dados.txt");
            String[] linhas = dados.split("\\n");
            for (String linha : linhas) {
                String[] partes = linha.split("#");
                if (partes.length == 4) {
                    int id = Integer.parseInt(partes[0]);
                    String nome = partes[1];
                    int inteiro = Integer.parseInt(partes[2]);
                    int decimo = Integer.parseInt(partes[3]);
                    list.append(id, nome, inteiro, decimo);
                }
            }
        } catch (Exception e) {
            System.out.println("Erro ao carregar dados.txt: " + e.getMessage());
        }
DLinkedList fixedList = Operation.map(list);

System.out.println(">>>>>>>>>> Dados convertidos para a nova representação dos dados >>>>>>>>>>");
System.out.println(fixedList);
System.out.println("<<<<<<<<<< Dados convertidos para a nova representação dos dados <<<<<<<<<<\n");

DLinkedList filteredGradedList = Operation.filterRemoveNonGraded(fixedList);
System.out.println(">>>>>>>>>> Lista filtrada (somente notas válidas) >>>>>>>>>>");
System.out.println(filteredGradedList);
System.out.println("<<<<<<<<<< Lista filtrada (somente notas válidas) <<<<<<<<<<\n");

DLinkedList filteredNonGradedList = Operation.filterRemoveGraded(fixedList);
System.out.println(">>>>>>>>>> Lista filtrada (somente 'ausência de nota') >>>>>>>>>>");
System.out.println(filteredNonGradedList);
System.out.println("<<<<<<<<<< Lista filtrada (somente 'ausência de nota') <<<<<<<<<<\n");

float average = Operation.reduce(filteredGradedList);
System.out.println(">>>>>>>>>> Média das notas válidas >>>>>>>>>>");
System.out.println(average);
System.out.println("<<<<<<<<<< Média das notas válidas <<<<<<<<<<\n");

DLinkedList aboveAverageList = Operation.filterRemoveBelowAverage(filteredGradedList, average);
System.out.println(">>>>>>>>>> Lista com notas acima da média >>>>>>>>>>");
System.out.println(aboveAverageList);
System.out.println("<<<<<<<<<< Lista com notas acima da média <<<<<<<<<<\n");

String contents = Operation.mapToString(fixedList);
System.out.println(">>>>>>>>>> Lista mapeada para uma única string >>>>>>>>>>");
System.out.println(contents);
System.out.println("<<<<<<<<<< Lista mapeada para uma única string <<<<<<<<<<\n");

try {
    Data.saveStringToTextFile("dados.csv", contents);
} catch (Exception e) {
    System.out.println("Erro ao salvar dados.csv: " + e.getMessage());
}
        DLinkedList testList = new DLinkedList();
        testList.insert("ABC", "John Doe", 4.7f);
        testList.append("XYZ", "Jane Doe", 9.9f);
        testList.insert("321", "Test", 2.3f);
        testList.append("Nothing", "Yada yada yada", 99.9f);
        testList.insert("qwerty", "QWERTY", 1.2f);
        testList.append("WASD", "wasd", 3.4f);
        testList.insert("ijkl", "IJKL", 5.6f);
        testList.append("1234", "Um Dois Tres Quatro", 7.8f);
        testList.clear();
    }
}
