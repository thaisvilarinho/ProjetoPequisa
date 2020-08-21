# coding: utf-8

import nltk
from nltk.metrics import ConfusionMatrix

''' Cada linha lida do arquivo contêm o texto do tweet e o nome do usuário. Recebemos a leitura completa do arquivo de 
texto e removemos o caracter de quebra de linha. Por fim, separamos cada linha do arquivo em campos que contenham o 
texto e nome usuário para serem armazenadas em uma estrutura array bidimensional,onde quando acessarmos pelos 
índices [x][0] teremos o texto de uma linha qualquer(x) e quando acessarmos pelos índices [x][1] teremos o nome 
do usuário. Exemplo: print(baseTreinamento[7000][0])'''


def carregarBases():
    global baseTreinamento
    global baseTeste
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
        definirStopWords()
        pegarRadicais(baseTreinamento, baseTeste)

    except IOError:
        print('Problemas com na leitura do arquivo')


def arquivarTextoSemStopWords(RegistroTweets):
    with open('textoSemStopWords.txt', 'w+') as arquivo:
        for (texto, usuario) in RegistroTweets:
            for palavra in texto.split():
                arquivo.write(str(palavra))
                arquivo.write("\n")

    arquivo.close()


'''Usa as stop words do nltk'''


def definirStopWords():
    global stopWordsNLTK
    stopWordsNLTK = nltk.corpus.stopwords.words('portuguese')
    stopWordsNLTK.append('vou')
    stopWordsNLTK.append('tão')


'''Remover os radicais das palavras e armazenas as palavras que não são spotWords
Aqui não há o controle de repetições'''


def pegarRadicais(registroTweetsTreinamento, registroTweetsTeste):
    global stopWordsNLTK
    pegaRadical = nltk.stem.RSLPStemmer()
    global registrosComRadicaisTreinamento
    global registrosComRadicaisTeste

    for (texto, usuario) in registroTweetsTreinamento:
        radicalTextoTreinamento = [str(pegaRadical.stem(palavra)) for palavra in texto.split() if
                                   palavra not in stopWordsNLTK]
        registrosComRadicaisTreinamento.append((radicalTextoTreinamento, usuario))

    for (texto, usuario) in registroTweetsTeste:
        radicalTextoTeste = [str(pegaRadical.stem(palavra)) for palavra in texto.split() if
                             palavra not in stopWordsNLTK]
        registrosComRadicaisTeste.append((radicalTextoTeste, usuario))

    listarSomenteRadicais(registrosComRadicaisTreinamento, registrosComRadicaisTeste)


'''Método pega somente os radicais extraídos do campo texto de cada tweet, ou seja, sem a classe do usuário 
associado. Assim vamos conseguir montar mais facilmente a tabela de caraterísticas do texto, usando os radicais
com cabeçalho'''


def listarSomenteRadicais(registrosComRadicaisTreinamento, registrosComRadicaisTeste):
    todosRadicaisTreinamento = []
    todosRadicaisTeste = []

    for (texto, usuario) in registrosComRadicaisTreinamento:
        todosRadicaisTreinamento.extend(texto)

    for (texto, usuario) in registrosComRadicaisTeste:
        todosRadicaisTeste.extend(texto)

    buscaFrequenciaRadicais(todosRadicaisTreinamento, todosRadicaisTeste)


'''Cria uma distribuição de frequência para a lista dos radicais das palavras e descobre quais são as mais 
importantes '''


def buscaFrequenciaRadicais(radicaisFrequentesTreinamento, radicaisTeste):
    radicaisFrequentesTreinamento = nltk.FreqDist(radicaisFrequentesTreinamento)
    radicaisFrequentesTeste = nltk.FreqDist(radicaisTeste)
    buscaRadicaisUnicos(radicaisFrequentesTreinamento, radicaisFrequentesTeste)


'''Gerar arquivo txt para visualizar radicais únicos gerados'''


def arquivarRadicaisUnicos(listaRadicaisUnicos):
    with open('radicais.txt', 'a') as arquivo:
        for radical in listaRadicaisUnicos:
            arquivo.write(radical)
            arquivo.write("\n")
    arquivo.close()


'''Remove os radicais repetidos e cria o cabeçalho da tabela de características'''


def buscaRadicaisUnicos(radicaisFrequentesTreinamento, radicaisFrequentesTeste):
    global radicaisUnicosTreinamento
    global radicaisUnicosTeste
    radicaisUnicosTreinamento = radicaisFrequentesTreinamento.keys()
    radicaisUnicosTeste = radicaisFrequentesTeste.keys()
    gerarBasesCompletas()

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
    global registrosComRadicalTreinamento
    global registrosComRadicalTeste
    baseCompletaTreinamento = nltk.classify.apply_features(extratorRadicais, registrosComRadicaisTreinamento)
    baseCompletaTeste = nltk.classify.apply_features(extratorRadicais, registrosComRadicaisTeste)
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
    registrosComRadicaisTreinamento = []
    registrosComRadicaisTeste = []
    radicaisUnicosTreinamento = []
    radicaisUnicosTeste = []

    carregarBases()

    # Gerar arquivos de texto para análise
    #arquivarTextoSemStopWords(baseTreinamento)
    #arquivarTextoSemStopWords(baseTeste)
    #arquivarRadicaisUnicos(radicaisUnicosTreinamento)
    #arquivarRadicaisUnicos(radicaisUnicosTeste)

