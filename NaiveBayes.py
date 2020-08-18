# coding: utf-8

import mysql.connector
from mysql.connector import Error
import nltk
import re
import numpy as np

basetreinamento = []
baseteste = []

stopwords = ['a', 'agora', 'algum', 'alguma', 'aquele', 'aqueles', 'de', 'deu', 'do', 'e', 'estou', 'esta', 'esta',
             'ir', 'meu', 'muito', 'mesmo', 'no', 'nossa', 'o', 'outro', 'para', 'que', 'sem', 'talvez', 'tem', 'tendo',
             'tenha', 'teve', 'tive', 'todo', 'um', 'uma', 'umas', 'uns', 'vou']

# usar as stop words do nltk
stopwordsnltk = nltk.corpus.stopwords.words('portuguese')
stopwordsnltk.append('vou')
stopwordsnltk.append('tão')

''' Cada linha lida do arquivo contêm o texto do tweet do usuário e o nome do usuário. Percorremos cada linha removendo
 o caracter de quebra de linha e separando texto e usuário para serem armazenadas em uma estrutura array bidimensional, 
 onde quando acessarmos pelos índices [x][0] teremos o texto de uma linha (x) e quando acessarmos pelos índices [x][1] 
 teremos o usuário. Exemplo: print(basePrincipal[7000][0])'''


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


    except IOError:
        print('Problemas com na leitura do arquivo')

    print("Tamanho base treinamento: ", len(basetreinamento))
    print("Tamanho base teste: ", len(baseteste))
    arquivo.close()


carregarBases()


def removestopwords(texto):
    frases = []
    for (palavras, usuario) in texto:
        semstop = [p for p in palavras.split() if p not in stopwordsnltk]
        frases.append((semstop, usuario))
    return frases


# print(removestopwords(base))

# Remover os radicais das palavras
def aplicastemmer(texto):
    print(texto)
    stemmer = nltk.stem.RSLPStemmer()
    frasessstemming = []
    for (palavras, usuario) in texto:
        comstemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwordsnltk]
        frasessstemming.append((comstemming, usuario))
    return frasessstemming


frasescomstemmingtreinamento = aplicastemmer(basetreinamento)
frasescomstemmingteste = aplicastemmer(baseteste)


# print(frasescomstemming)

def buscapalavras(frases):
    todaspalavras = []
    for (palavras, usuario) in frases:
        todaspalavras.extend(palavras)
    return todaspalavras


palavrastreinamento = buscapalavras(frasescomstemmingtreinamento)
palavrasteste = buscapalavras(frasescomstemmingteste)


# print(palavras)

def buscafrequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras


frequenciatreinamento = buscafrequencia(palavrastreinamento)
frequenciateste = buscafrequencia(palavrasteste)


# print(frequencia.most_common(50))

def buscapalavrasunicas(frequencia):
    freq = frequencia.keys()
    return freq


palavrasunicastreinamento = buscapalavrasunicas(frequenciatreinamento)
palavrasunicasteste = buscapalavrasunicas(frequenciateste)


# print(palavrasunicastreinamento)

# print(palavrasunicas)

def extratorpalavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavrasunicastreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])
# print(caracteristicasfrase)

basecompletatreinamento = nltk.classify.apply_features(extratorpalavras, frasescomstemmingtreinamento)
basecompletateste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingteste)
# print(basecompleta[15])

# constroi a tabela de probabilidade
classificador = nltk.NaiveBayesClassifier.train(basecompletatreinamento)
print(classificador.labels())
# print(classificador.show_most_informative_features(20))

print(nltk.classify.accuracy(classificador, basecompletateste))

erros = []
for (frase, classe) in basecompletateste:
    # print(frase)
    # print(classe)
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

teste = 'eu sinto medo por voce'
testestemming = []
stemmer = nltk.stem.RSLPStemmer()
for (palavrastreinamento) in teste.split():
    comstem = [p for p in palavrastreinamento.split()]
    testestemming.append(str(stemmer.stem(comstem[0])))
# print(testestemming)

novo = extratorpalavras(testestemming)
# print(novo)

# print(classificador.classify(novo))
distribuicao = classificador.prob_classify(novo)
# for classe in distribuicao.samples():
#    print("%s: %f" % (classe, distribuicao.prob(classe)))
