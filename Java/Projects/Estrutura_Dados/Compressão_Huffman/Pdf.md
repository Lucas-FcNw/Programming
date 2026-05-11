## Projeto 1 de Estrutura de Dados II

Compressão de Arquivos com oAlgoritmo de Human

### Prof. Dr.JeanM.Laine

- 1 Intro dução Conteúdo
- 2 Ob jetivosdoPro jeto
- 3 DescriçãoDetalhadadoAlgoritmo
   - 3.1 Parte1:OPro cessodeCompressão
      - 3.1.1 Passo1: AnálisedeFrequência
      - 3.1.2 Passo2: AFiladePrioridades(Min-Heap).
      - 3.1.3 Passo3: ConstruçãodaÁrvoredeHuman
      - 3.1.4 Passo4: GeraçãodaTab eladeCó digos.
      - 3.1.5 Passo5: Co dicaçãoeEscritadoArquivo
   - 3.2 Parte2:OPro cessodeDescompressão
   - 3.3 Parte3:OPercursonaDescompressão
- 4 ExemploCompletoPassoaPasso
   - 4.1 Passo1:AnálisedeFrequência
   - 4.2 Passo2:ConstruçãodaÁrvoreviaMin-Heap
   - 4.3 Passo3:ÁrvoredeHumanFinal.
   - 4.4 Passo4:Tab eladeCó digosResultante
   - 4.5 Passo5:Co dicação
   - 4.6 Passo6:Descompressão(UsandooPercursoGuiado)
- 5 SaídaEsp eradadoPrograma
- 6 RequisitosdeImplementação,EntregaeObservaçõ es
- 7 AnálisesRequeridas
- 8 CritériosdeAvaliação
- 9 ReferênciaseMaterialdeAp oio


## 1 Intro dução Conteúdo

OAlgoritmodeHumané umméto dodecompressãosemp erdasqueatribuicó digos
detamanhovariávelaoscaracteresdeentradacombaseemsuasfrequências. Caracte-
resfrequentesreceb em có digoscurtos ecaracteresraros receb emcó digos maislongos,
otimizandootamanhonaldoarquivo.
Emb orasejaumalgoritmoclássico,suarelevânciap ersisteatého je,sendoumcom-
p onentefundamentalemdiversastecnologiasqueusamosdiariamente. Entenderoseu
funcionamentoécompreenderumadasbasesdatransmissãoearmazenamentoeciente
dedados.Algumasdesuasaplicaçõ esmaisnotáveisincluem:

```
 CompressãodeArquivos(.zip,.gzip):Op opularalgoritmoDEFLATE,queé
ocoraçãodosformatosZIPeGZIP,utilizaumacombinaçãodoalgoritmoLZ77com
aco dicaçãodeHuman. OHumanéaetapanalresp onsávelp orcomprimirde
formaecienteosdadosjápro cessadosp eloLZ77.
```
```
 FormatosdeImagem(JPEG,PNG):NoformatoJPEG,ap ósas transformaçõ es
matemáticasquepro cessamascoresdaimagem,aco dicaçãodeHumanéusada
paracomprimirosco ecientesresultantes,reduzindodrasticamenteotamanhodo
arquivo. NoformatoPNG,oHumantamb éméumcomp onenteessencialdoseu
méto dodecompressãosemp erdas.
```
```
 FormatosdeÁudioeVídeo(MP3,MPEG):Padrõ esdecompressãodemídiacomo
MP3eMPEGusamvariaçõ esdaco dicaçãodeHumancomoumadesuasetapas
naispararepresentarosdadosdeáudioevídeodeformacompacta.
```
```
 Proto colosdeRede(HTTP/2):Paratornaranavegaçãonawebmaisrápida,
o proto coloHTTP/2 usao HPACK paracompressão de cab eçalhos. Uma das
estratégias do HPACKé usarumatab ela deHuman estáticapararepresentar
stringscomunsnoscab eçalhosHTTP,reduzindoaquantidadededadostransmitidos
entreonavegadoreoservidor.
```
Portanto, aoimplementaroalgoritmodeHumanedesenvolverestepro jeto,vo cês
nãoestarãoap enaspraticandoconceitosdeestruturasdedadoseosusandopararesolver
problemas,mastamb émrecriandoumap eçadetecnologiaqueéabaseparaatransmissão
eoarmazenamentoecientededadosnacomputaçãomo derna.

## 2 Ob jetivosdoPro jeto

```
 ImplementareutilizarumaFiladePrioridades(Min-Heap).
```
```
 Mo delar,construirep ercorrerumaÁrvoreBinária(aÁrvoredeHuman).
```
```
 Desenvolverumaaplicaçãodelinhadecomandoparacompressãoedescompressão.
```
```
 Gerar um novoarquivocomos dados comprimidose ser capazdereconstruir o
arquivooriginalapartirdele.
```
```
 ManipulararquivosemníveldeleituraeescritaemJava.
```
```
 Praticarotrabalhoemequip e(máximo 4 emínimo 3 alunosp orgrup o)eadivisão
detarefas.
```

## 3 DescriçãoDetalhadadoAlgoritmo

Opro jetoédivididoemfuncionalidadesprincipais.Umademonstraçãocompletacomum
exemplopráticoédetalhadanaSeção4.

### 3.1 Parte1:OPro cessodeCompressão

#### 3.1.1 Passo1: AnálisedeFrequência

Leiaoarquivodeentradaeconteafrequênciadecadacaractere. Paraisso,vo cêdeve
utilizarumvetordeinteiros(int[])detamanho 256 (paracobriratab elaASCI I).

#### 3.1.2 Passo2: AFiladePrioridades(Min-Heap).

Vo cêdeveráimplementarumaFiladePrioridadesusandoumMin-Heap.

Nota ConceitualImp ortante: Écrucialentenderadiferençaentreaideiadeum
Min-Heapesuaimplementação.

```
 Conceitualmente: UmMin-Heapéumaárvorebináriacompleta.
```
```
 Na Prática: RepresentamosessaárvoreusandoumvetorouArrayList. Para
umnónoíndicei,seulhoesquerdoestáem2*i + 1,odireitoem2*i + 2,eo
paiem(i - 1) / 2.
```
SuaclasseMinHeapconteráumArrayList<No>.

EstruturadoNó: AclasseNoseráusadaparaconstruiraÁrvoredeHuman.

```
class No implements Comparable<No> {
char caractere;
int frequencia;
No esquerda, direita;
// Implementar construtor e o metodo compareTo
@Override
public int compareTo(No outroNo) {
return this.frequencia - outroNo.frequencia;
}
}
```
AnalisandoaClasseNo: Estaclasseéabaseparaasduasestruturasdopro jeto.

```
 char caractere, int frequencia:Guardamosdadosessenciaisdecadafolhada
árvore:ocaractereemsiequantasvezeseleapareceu.
```
```
 No esquerda, No direita:Sãoasreferências(p onteiros)usadasparaconstruira
ÁrvoredeHumannal. Notequeestesatributosp ertencemàárvoreexplícita
queserágerada,enãoàestruturadoMin-Heap(queéimplícita,emumvetor).
```
```
 implements Comparable<No>: Éo"contrato"queaclassefazaoJava,garantindo
queob jetosdotip oNosab emcomosecomparare,p ortanto,p o demserordenados.
```

```
 compareTo(No outroNo): Éaimplementaçãodaquelecontrato. Esteméto doéo
"cérebro"dacomparação,sendoinvo cadop eloMin-Heapparadecidirqualnótem
amenorfrequência(e,p ortanto,maiorprioridade).
```
#### 3.1.3 Passo3: ConstruçãodaÁrvoredeHuman

EnquantooMin-Heaptivermaisdeumnó,removaosdoisdemenorfrequência,combine-
osemumnovonóinternoeinsiraestenovonódevoltanoheap.

#### 3.1.4 Passo4: GeraçãodaTab eladeCó digos.

Comaárvorecompleta,p ercorra-arecursivamente.Paraarmazenaratab ela,utilizeum
vetordeStrings(String[])detamanho 256.

#### 3.1.5 Passo5: Co dicaçãoeEscritadoArquivo

Aonaldo pro cesso,oprogramadevegerar um novo arquivo desaída(ex: com
extensão.huff).Estearquivodeveconterumcab eçalho(comatab eladefrequências)
eosdadoscomprimidos.

### 3.2 Parte2:OPro cessodeDescompressão

Opro cessodedescompressãoconsisteemreconstruiraárvoreapartirdocab eçalhode
umarquivopreviamentecomprimidoe,emseguida,usaressaárvoreparadeco dicaro
uxodebits,gerandooarquivooriginal.

### 3.3 Parte3:OPercursonaDescompressão

Adescompressãoutilizaumméto dodep ercurso,masdeumaformadiferentedosp ercur-
soscompletoscomoPré-OrdemouEm-Ordem.Emvezdevisitarto dososnósdaárvore
deumasóvez,adescompressãorealizaum**"p ercursoguiadop elosdados"**.
Funcionadaseguinteforma:

1. ComecenaraizdaárvoredeHuman.
2. Leiaumbitdoarquivocomprimido.Sefor'0',desçaparaolhodaesquerda.Se
    for'1',desçaparaadireita.
3. Veriqueseonóatualéumafolha.

```
 Senãoforumafolha,repitaopasso2.
 Seforumafolha,vo cêdeco dicouumcaractere! Escrevaocaracterenoarquivo
desaída.
```
4. Ap ósdeco dicarumcaractere,volteparaaraizerepitato doopro cessoapartir
    dopasso 1 paraopróximocaractere.

Esteciclode"p ercursoscurtos"(daraizatéumafolha)continuaatéqueto doouxode
bitsdoarquivocomprimidotenhasidoconsumido.


## 4 ExemploCompletoPassoaPasso

Vamosusarumexemplosimples. Imaginequeseuarquivodeentrada(.txt),tenhauma
únicalinhacomapalavra"BANANA",ap enas.Vamosusaresteexemploparailustrar
to doopro cesso.

### 4.1 Passo1:AnálisedeFrequência

Ap óslerastring"BANANA",ovetordefrequênciasconteráosseguintesvalores(outras
p osiçõ essão0):

```
 frequencias['B'] = 1
```
```
 frequencias['A'] = 3
```
```
 frequencias['N'] = 2
```
### 4.2 Passo2:ConstruçãodaÁrvoreviaMin-Heap

Primeiro,criamososnósfolhaeosinserimosnoMin-Heap. Oheap(representadocomo
umvetor)éordenadop elafrequência.

EstadoInicialdoHeap:

```
Vetor do Heap: [ No('B',1), No('N',2), No('A',3) ]
```
Iteração1: RemovemosNo('B',1)eNo('N',2),criamosumnópaiN1comfrequência
3 (1+2),eoinserimosdevolta.

EstadodoHeapap ósaIteração1:

```
Vetor do Heap: [ No('A',3), N1(freq:3) ]
```
Iteração2: RemovemosNo('A',3)eN1(freq:3),criamosonóRAIZcomfrequência
6 (3+3),eoinserimosdevolta.Opro cessotermina.

### 4.3 Passo3:ÁrvoredeHumanFinal.

Aestruturadaárvoreresultanteé:

```
(RAIZ, 6)
/ \
('A', 3) (N1, 3)
/ \
('B',1) ('N',2)
```

### 4.4 Passo4:Tab eladeCó digosResultante

Percorrendoaárvore(esquerda='0',direita='1'):

```
 A:`0`
```
```
 B:`10`
```
```
 N:`11`
```
### 4.5 Passo5:Co dicação

"BANANA-> 100110110 (9bits). Comparação: Original(ASCI I)= 6 caracteres* 8
bits= 48 bits. Economiasignicativa.

### 4.6 Passo6:Descompressão(UsandooPercursoGuiado)

Paradeco dicar 100110110 :

```
 Começanaraiz.Lê 10 ->Cheganafolha'B'.EscreveB.Voltaparaaraiz.
```
```
 Lê 0 ->Cheganafolha'A'.EscreveA.Voltaparaaraiz.
```
```
 Lê 11 ->Cheganafolha'N'.EscreveN.
```
```
 ...eassimp ordianteatéreconstruir"BANANA".
```

## 5 SaídaEsp eradadoPrograma

Parafacilitar acorreçãoe adepuração, seu programadeveimprimiras estruturas de
dadosintermediáriasnoconsole (System.out)durante opro cessodecompressão. A
impressãodeveseguiroformatodoexemploabaixo.

ExemplodeSaídaparaoarquivocom"BANANA":

```
--------------------------------------------------
ETAPA 1: Tabela de Frequencia de Caracteres
--------------------------------------------------
Caractere 'B' (ASCII: 66): 1
Caractere 'A' (ASCII: 65): 3
Caractere 'N' (ASCII: 78): 2
```
##### --------------------------------------------------

```
ETAPA 2: Min-Heap Inicial (Vetor)
--------------------------------------------------
[ No('B',1), No('N',2), No('A',3) ]
```
##### --------------------------------------------------

```
ETAPA 3: Arvore de Huffman
--------------------------------------------------
```
- (RAIZ, 6)
    - ('A', 3)
    - (N1, 3)
       - ('B', 1)
       - ('N', 2)

##### --------------------------------------------------

```
ETAPA 4: Tabela de Codigos de Huffman
--------------------------------------------------
Caractere 'A': 0
Caractere 'B': 10
Caractere 'N': 11
```
##### --------------------------------------------------

```
ETAPA 5: Resumo da Compressao
--------------------------------------------------
Tamanho original....: 48 bits (6 bytes)
Tamanho comprimido..: 9 bits (2 bytes)
Taxa de compressao..: 81.25%
--------------------------------------------------
```

## 6 RequisitosdeImplementação,EntregaeObservaçõ es

```
 Linguagem:Opro jetodeveserimplementadoemJava.Adicioneonomecompleto
dosintegrantesdogrup onocab eçalhodo(s)arquivo(s).
```
```
 Op eraçãodeArquivos: Oprogramanuncadevemo dicaroarquivodeentrada
original. Acompressãodevesempregerarumnovoarquivodesaída,eadescom-
pressãotamb ém.
```
```
 Execução:Oprogramaqueserátestadodeveserexecutávelvialinhadecomandoe
teronomehuman.jar.Asexecuçõ esetestesdeverãoserfeitosatravésdosseguintes
comandos:
```
```
# Para comprimir
java -jar huffman.jar -c <arquivo_original> <arquivo_comprimido>
```
```
# Para descomprimir
java -jar huffman.jar -d <arquivo_comprimido> <arquivo_restaurado>
```
```
 Relatório:UmrelatórioemPDF(mínimode 3 emáximode 6 páginas)explicando
as decisõ es depro jetoe a implementação dasestruturas de dados. O relatório
deveobrigatoriamenteconteraseçãode"AnálisesRequeridas",apresentando as
tab elas/grácoseasdiscussõ essobreap erformanceeastaxasdecompressão.
```
```
 Entrega:Có digo-fontecompletodopro jetoJava(.java),oarquivohuman.jare
orelatório.
```
```
 Apresentação:Apresentaropro jetoéobrigatórioparaanota.
```
## 7 AnálisesRequeridas

Orelatórionaldeveconteras seguintesanálisesexp erimentaissobreoseuprograma.
Paragarantirumabasedecomparaçãoconsistenteentreto dososgrup os,seráfornecido
umarquivodetextopadrão,chamadoarq_de_teste.txt. Asanálisesdep erformancee
taxadecompressãoparatextocomumdevemserrealizadasutilizandoestearquivoe
do cumentadasnorelatório.Asanálisescomosoutrostip osdearquivo(có digo-fonte,
etc.)continuamsendoimp ortantesparaumaavaliaçãomaisamplaecompleta.

Parte1: AnálisedePerformance(Temp o):

```
 O que fazer? Meçaotemp o deexecução (emmilissegundos) dassuasfunçõ es
decompressãoedescompressão. Testecomarquivosdetextodediferentestama-
nhos (ex: 1KB, 100KB, 1MB, 10MB).Para medir otemp o em Java, use `Sys-
tem.nanoTime()`.
```
```
 O quedo cumentarnorelatório? Umaseçãocontendoumatab elaougráco
mostrandoarelaçãoentreotamanhodoarquivoeotemp odeexecução. Discuta
seocrescimentodotemp oé lineare secorresp ondeaoesp eradop elaanálisede
complexidadeteóricadoalgoritmo.
```

Parte2: ComparaçãodeTaxasdeCompressão(Espaço):

```
 Oquefazer? Calculeataxadecompressãoparadiferentestip osdearquivo. A
taxap o desercalculadacomafórmula:
```
```
TaxadeCompressão=
```
##### 

##### 1 −

```
TamanhoComprimido
TamanhoOriginal
```
##### 

##### ×100%

```
Testecomarquivosdetextodecaracterísticasvariadas, como: umtexto comum
(capítulodelivro),umcó digo-fonte(.java),umarquivomuitorep etitivo(ex:"AA-
AAA...")eumarquivocomcaracteresaleatórios.
```
```
 Oquedo cumentarnorelatório? Umatab elamostrandoataxadecompressão
paracadatip odearquivotestado. Omais imp ortanteéasuaanálise: explique
p orqueastaxasvariaram. Porqueoarquivorep etitivocomprimiutãob em? Por
queoarquivoaleatórioteveumacompressãoruimouaténegativa(aumentoude
tamanho)? Suaanálisedevedemonstrarquevo cêentendeuquando ep or queo
algoritmodeHumanéeciente.
```
## 8 CritériosdeAvaliação

Aavaliaçãodo pro jetoserá baseadana rubrica detalhadanaTab ela 1. Ap ontuação
totaléde10,0p ontos,distribuídosentreoscritériosdefuncionalidade,implementação
dasestruturasdedados,equalidadegeraldocó digoedorelatório.

## 9 ReferênciaseMaterialdeAp oio

```
 Co dicaçãodeHuman:
https://www.ime.usp.br/ pf/estruturas-de-dados/aulas/huffman.html
```
```
 GeeksforGeeks-HeapDataStructure:
https://www.geeksforgeeks.org/heap-data-structure/
```
```
 GeeksforGeeks-PriorityQueueemJava
https://www.geeksforgeeks.org/java/priority-queue-in-java/
```
```
 Livro-Algoritmos:TeoriaePrática
CORMEN,ThomasH.etal. Algoritmos: TeoriaePrática. 3 ªed.RiodeJaneiro:
LTC,2012.
```

```
Tab ela1: RubricadeAvaliaçãodoPro jeto
```
Categoria Subitem CritériodeAvaliação Pontos

1. Funcio-
nalidade e
Corretude
(6,0)

```
1.1CompilaçãoeExecução O programa compila e executa
semerrosconforme a esp ecica-
ção.
```
##### 1,

```
1.2Compressão Geratab elascorretas(frequência,
có digos),saídanoconsolenofor-
matocorretoecriaoarquivode
saída.
```
##### 2,

```
1.3Descompressão Oarquivo descomprimidoép er-
feitamente idêntico ao original;
lida com erros de arquivo invá-
lido.
```
##### 2,

2. Imple-
mentação
das Estru-
turas(2,0)

```
2.1Min-Heap Implementado com ve-
tor/ArrayList e com op eraçõ es
ecientes(logarítmicas).
```
##### 1,

```
2.2ÁrvoredeHuman ClasseNoealgoritmodeconstru-
çãodaárvoreestãocorretos.
```
##### 1,

3. Quali-
dadeeRela-
tório(2,0)

```
3.1QualidadedoCó digo Có digo b emorganizado, comen-
tado, comb onsnomesdevariá-
veis/méto dos.
```
##### 1,

```
3.2RelatórioeAnálises Relatório claro e b em estrutu-
rado,contendoasanálisesreque-
ridas.
```
##### 1,

##### TOTAL 10,


