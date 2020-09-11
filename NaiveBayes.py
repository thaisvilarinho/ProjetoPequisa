# coding: utf-8

import nltk
from nltk.metrics import ConfusionMatrix


def gerarArquivoSemStopWords(listaSemStopWords):
    with open('textoSemStopWords.txt', 'w+', encoding="utf-8") as arquivo:
        for (texto, usuario) in listaSemStopWords:
            for palavra in texto.split():
                if palavra not in stopWordsNLTK:
                    arquivo.write(str(palavra))
                    arquivo.write("\n")

    arquivo.close()


def arquivarRadicaisUnicos(listaRadicaisUnicos):
    with open('radicais.txt', 'a', encoding="utf-8") as arquivo:
        for radical in listaRadicaisUnicos:
            arquivo.write(radical)
            arquivo.write("\n")
    arquivo.close()


def arquivarErros():
    global erros
    with open('erros.txt', 'a', encoding="utf-8") as arquivo:
        for classe, resultado, frase in erros:
            arquivo.write(classe + ',' + resultado + ',' + str(frase))
            arquivo.write("\n")
    arquivo.close()


def carregarBases():
    global baseTreinamento
    global baseTeste
    try:
        with open('baseTreinamento.txt', 'r', encoding="utf-8") as arquivo:
            for linha in arquivo.readlines():
                linha = linha.split('#')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                baseTreinamento.append(registro)

        with open('baseTeste.txt', 'r', encoding="utf-8") as arquivo:
            for linha in arquivo.readlines():
                linha = linha.split('#')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                baseTeste.append(registro)

        arquivo.close()
        atualizarListaStopWords()
        pegarRadicais(baseTreinamento, baseTeste)

    except IOError:
        print('Problemas com na leitura do arquivo')


def atualizarListaStopWords():
    global stopWordsNLTK
    with open('listaStopWords.txt', 'r+') as arquivo:
        for palavra in arquivo.readlines():
            stopWordsNLTK.append(palavra)

    arquivo.close()


'''Remover os radicais das palavras e armazenas as palavras que não são spotWords'''


def pegarRadicais(registroTweetsTreinamento, registroTweetsTeste):
    global stopWordsNLTK
    global registrosComRadicaisTreinamento
    global registrosComRadicaisTeste
    pegaRadical = nltk.stem.RSLPStemmer()

    for (texto, usuario) in registroTweetsTreinamento:
        radicalTextoTreinamento = [str(pegaRadical.stem(palavra)) for palavra in texto.split() if
                                   palavra not in stopWordsNLTK]
        registrosComRadicaisTreinamento.append((radicalTextoTreinamento, usuario))

    for (texto, usuario) in registroTweetsTeste:
        radicalTextoTeste = [str(pegaRadical.stem(palavra)) for palavra in texto.split() if
                             palavra not in stopWordsNLTK]
        registrosComRadicaisTeste.append((radicalTextoTeste, usuario))

    listarSomenteRadicais(registrosComRadicaisTreinamento, registrosComRadicaisTeste)


'''Pegar somente os radicais para facilitar montar o vetor de características'''


def listarSomenteRadicais(registrosComRadicaisTreinamento, registrosComRadicaisTeste):
    todosRadicaisTreinamento = []
    todosRadicaisTeste = []

    for (texto, usuario) in registrosComRadicaisTreinamento:
        todosRadicaisTreinamento.extend(texto)

    for (texto, usuario) in registrosComRadicaisTeste:
        todosRadicaisTeste.extend(texto)

    buscaFrequenciaRadicais(todosRadicaisTreinamento, todosRadicaisTeste)


def buscaFrequenciaRadicais(radicaisFrequentesTreinamento, radicaisTeste):
    radicaisFrequentesTreinamento = nltk.FreqDist(radicaisFrequentesTreinamento)
    radicaisFrequentesTeste = nltk.FreqDist(radicaisTeste)
    buscaRadicaisUnicos(radicaisFrequentesTreinamento, radicaisFrequentesTeste)


'''Remove os radicais repetidos e cria o cabeçalho da tabela de características'''


def buscaRadicaisUnicos(radicaisFrequentesTreinamento, radicaisFrequentesTeste):
    global radicaisUnicosTreinamento
    global radicaisUnicosTeste
    radicaisUnicosTreinamento = radicaisFrequentesTreinamento.keys()
    radicaisUnicosTeste = radicaisFrequentesTeste.keys()
    gerarBasesCompletas()


def extrairCaracteristicas(documento):
    global radicaisUnicosTreinamento
    doc = set(documento)
    caracteristicas = {}
    for palavras in radicaisUnicosTreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


def gerarBasesCompletas():
    baseCompletaTreinamento = nltk.classify.apply_features(extrairCaracteristicas, registrosComRadicaisTreinamento)
    baseCompletaTeste = nltk.classify.apply_features(extrairCaracteristicas, registrosComRadicaisTeste)
    treinamento(baseCompletaTreinamento, baseCompletaTeste)


def treinamento(baseCompletaTreinamento, baseCompletaTeste):
    classificador = nltk.NaiveBayesClassifier.train(baseCompletaTreinamento)
    print("Acurácia: ", nltk.classify.accuracy(classificador, baseCompletaTeste))
    verificarErros(classificador, baseCompletaTeste)
    gerarMatrizConfusao(classificador, baseCompletaTeste)


def verificarErros(classificador, baseCompletaTeste):
    for (frase, classe) in baseCompletaTeste:
        resultado = classificador.classify(frase)
        if resultado != classe:
            erros.append((classe, resultado, frase))


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
    stopWordsNLTK = nltk.corpus.stopwords.words('portuguese') + nltk.corpus.stopwords.words('english')
    registrosComRadicaisTreinamento = []
    registrosComRadicaisTeste = []
    radicaisUnicosTreinamento = []
    radicaisUnicosTeste = []
    erros = []

    carregarBases()

    # Gerar arquivos
    # arquivarErros()
    # gerarArquivoSemStopWords(baseTreinamento)
    # gerarArquivoSemStopWords(baseTeste)
    # arquivarRadicaisUnicos(radicaisUnicosTreinamento)
    # arquivarRadicaisUnicos(radicaisUnicosTeste)
