# coding: utf-8

import nltk
from nltk.metrics import ConfusionMatrix


''' Cada linha lida do arquivo contêm o texto do tweet e o nome do usuário. Recebemos a leitura completa do arquivo de 
texto e removemos o caracter de quebra de linha. Por fim, separamos cada linha do arquivo em campos que contenham o 
texto e nome usuário para serem armazenadas em uma estrutura array bidimensional,onde quando acessarmos pelos 
índices [x][0] teremos o texto de uma linha qualquer(x) e quando acessarmos pelos índices [x][1] teremos o nome 
do usuário. Exemplo: print(basePrincipal[7000][0])
Manter uma array bidimensional é necessária para aplicarmos o treinamento da base que gerará o modelo do algoritmo
Naive Bayes e assim conseguirmos aplicar o teste para verificarmos a acurácia.'''


def carregarBases():
    try:
        with open('baseTreinamento.txt', 'r') as arquivo:
            for linha in arquivo.readlines():
                linha = linha.split(',')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                baseTreinamento.append(registro)

        with open('baseTeste.txt', 'r') as arquivo:
            for linha in arquivo.readlines():
                linha = linha.split(',')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                baseTeste.append(registro)

        arquivo.close()

    except IOError:
        print('Problemas com na leitura do arquivo')


def definirStopWords():
    global stopWordsNLTK
    # usar as stop words do nltk
    stopWordsNLTK = nltk.corpus.stopwords.words('portuguese')
    stopWordsNLTK.append('vou')
    stopWordsNLTK.append('tão')


'''Remover os radicais das palavras e armazenas as palavras que não são spotWords
Aqui não há o controle de repetições'''


def pegarRadicais(RegistroTweet):
    global stopWordsNLTK
    pegaRadical = nltk.stem.RSLPStemmer()
    listaTextoRadicais = []
    for (texto, usuario) in RegistroTweet:
        textoSomenteRadical = [str(pegaRadical.stem(palavra)) for palavra in texto.split() if
                               palavra not in stopWordsNLTK]
        listaTextoRadicais.append((textoSomenteRadical, usuario))
    return listaTextoRadicais


'''Método pega somente os radicais extraídos do campo texto de cada tweet, ou seja, sem a classe do usuário 
associado. Assim vamos conseguir montar mais facilmente a tabela de caraterísticas do texto, usando os radicais
com cabeçalho'''


def listarSomenteRadicais(RegistrosTweets):
    todosRadicais = []
    for (texto, usuario) in RegistrosTweets:
        todosRadicais.extend(texto)
    return buscaFrequenciaRadicais(todosRadicais)


'''Cria uma distribuição de frequência para a lista dos radicais das palavras e descobre quais são as mais 
importantes '''


def buscaFrequenciaRadicais(radicais):
    radicais = nltk.FreqDist(radicais)
    return buscaRadicaisUnicos(radicais)


'''Remove os radicais repetidos e cria o cabeçalho da tabela de características'''


def buscaRadicaisUnicos(frequencia):
    freq = frequencia.keys()
    return freq


'''Método recebe os radicais e repassa para uma coleção SET que irá manter a lista sem repetições.
Por fim é percorrido cada elemetno do vetor de características e os compara com cada radical, 
para assim saber se os radicais constam ou não dentro do vetor. E assim é montado o cabeçalho da tabela
de características'''


def extratorRadicais(documento):
    global radicaisUnicosTreinamento
    doc = set(documento)
    caracteristicas = {}
    for palavras in radicaisUnicosTreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


def gerarBasesCompletas():
    baseCompletaTreinamento = nltk.classify.apply_features(extratorRadicais, registrosComRadicalTreinamento)
    baseCompletaTeste = nltk.classify.apply_features(extratorRadicais, registrosComRadicalTeste)
    treinamento(baseCompletaTreinamento, baseCompletaTeste)


''' Gerará a tabela de probabilidade com algoritmo Naive Bayes utilizando a base de treinamento, ou seja
geramos o modelo que será utilizado para verificar a acurácia'''


def treinamento(baseCompletaTreinamento, baseCompletaTeste):
    classificador = nltk.NaiveBayesClassifier.train(baseCompletaTreinamento)
    print("Acurácia: ", nltk.classify.accuracy(classificador, baseCompletaTeste))
    verificarErros(classificador, baseCompletaTeste)
    gerarMatrizConfusao(classificador, baseCompletaTeste)


def verificarErros(classificador, baseCompletaTeste):
    erros = []
    for (frase, classe) in baseCompletaTeste:
        resultado = classificador.classify(frase)
        if resultado != classe:
            erros.append((classe, resultado, frase))
    # for (classe, resultado, frase) in erros:
    #    print(classe, resultado, frase)


def gerarMatrizConfusao(classificador, baseCompletaTeste):
    esperado = []
    previsto = []
    for (frase, classe) in baseCompletaTeste:
        resultado = classificador.classify(frase)
        previsto.append(resultado)
        esperado.append(classe)

    matriz = ConfusionMatrix(esperado, previsto)
    print(matriz)


if __name__ == "__main__":
    baseTreinamento = []
    baseTeste = []
    stopWordsNLTK = ''

    carregarBases()
    definirStopWords()
    registrosComRadicalTreinamento = pegarRadicais(baseTreinamento)
    registrosComRadicalTeste = pegarRadicais(baseTeste)
    radicaisUnicosTreinamento = listarSomenteRadicais(registrosComRadicalTreinamento)
    radicaisUnicosTeste = listarSomenteRadicais(registrosComRadicalTeste)
    gerarBasesCompletas()

