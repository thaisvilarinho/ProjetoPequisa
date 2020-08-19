# coding: utf-8

import nltk

basetreinamento = []
baseteste = []

# usar as stop words do nltk
stopWordsNLTK = nltk.corpus.stopwords.words('portuguese')
stopWordsNLTK.append('vou')
stopWordsNLTK.append('tão')

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
                basetreinamento.append(registro)

        with open('baseTeste.txt', 'r') as arquivo:
            for linha in arquivo.readlines():
                linha = linha.split(',')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                baseteste.append(registro)

        arquivo.close()
    except IOError:
        print('Problemas com na leitura do arquivo')


carregarBases()

'''Remover os radicais das palavras'''


def aplicaRemocaoRadical(RegistroTweet):
    removeRadica = nltk.stem.RSLPStemmer()
    listaTextoSemRadical = []
    for (texto, usuario) in RegistroTweet:
        textoRemovidoRadical = [str(removeRadica.stem(palavra)) for palavra in texto.split() if palavra not in stopWordsNLTK]
        listaTextoSemRadical.append((textoRemovidoRadical, usuario))
    return listaTextoSemRadical


frasescomstemmingtreinamento = aplicaRemocaoRadical(basetreinamento)
frasescomstemmingteste = aplicaRemocaoRadical(baseteste)


def buscapalavras(frases):
    todaspalavras = []
    for (palavras, usuario) in frases:
        todaspalavras.extend(palavras)
    return todaspalavras


palavrastreinamento = buscapalavras(frasescomstemmingtreinamento)
palavrasteste = buscapalavras(frasescomstemmingteste)


def buscafrequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras


frequenciatreinamento = buscafrequencia(palavrastreinamento)
frequenciateste = buscafrequencia(palavrasteste)


def buscapalavrasunicas(frequencia):
    freq = frequencia.keys()
    return freq


palavrasunicastreinamento = buscapalavrasunicas(frequenciatreinamento)
palavrasunicasteste = buscapalavrasunicas(frequenciateste)


def extratorpalavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavrasunicastreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])

basecompletatreinamento = nltk.classify.apply_features(extratorpalavras, frasescomstemmingtreinamento)
basecompletateste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingteste)

# constroi a tabela de probabilidade
classificador = nltk.NaiveBayesClassifier.train(basecompletatreinamento)

print("Acurácia: ", nltk.classify.accuracy(classificador, basecompletateste))

erros = []
for (frase, classe) in basecompletateste:
    resultado = classificador.classify(frase)
    if resultado != classe:
        erros.append((classe, resultado, frase))
# for (classe, resultado, frase) in erros:
#    print(classe, resultado, frase)

from nltk.metrics import ConfusionMatrix

esperado = []
previsto = []
for (frase, classe) in basecompletateste:
    resultado = classificador.classify(frase)
    previsto.append(resultado)
    esperado.append(classe)

matriz = ConfusionMatrix(esperado, previsto)
print(matriz)

# 1. Cenário
# 2. Número de classes
# 3. ZeroRules

teste = 'eu amo meu país'
testestemming = []
stemmer = nltk.stem.RSLPStemmer()
for (palavrastreinamento) in teste.split():
    comstem = [p for p in palavrastreinamento.split()]
    testestemming.append(str(stemmer.stem(comstem[0])))

novo = extratorpalavras(testestemming)
distribuicao = classificador.prob_classify(novo)
