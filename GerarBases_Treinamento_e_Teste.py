# -*- coding: utf-8 -*-
from sklearn.model_selection import train_test_split

basePrincipal = []
baseTreinamento = []
baseTeste = []
totalRegistrosPegar = 1000
PorentagemBaseTeste = 0.3

'''Ler arquivo base que contêm os dados de texto e nome de usuário de cada tweeet que foi armazenado no 
 banco de dados e gera um arquivo com 70% para base de treinamento e 30% para a base de testes que serão
 usados no algortimo Naive Bayes'''


def escreverArquivos():
    baseTreinamento, baseTeste = train_test_split(basePrincipal, test_size=PorentagemBaseTeste)

    print("Tamanho base principal: ", len(basePrincipal))
    print("Tamanho base treinamento: ", len(baseTreinamento))
    print("Tamanho base teste: ", len(baseTeste))

    try:
        with open("baseTreinamento.txt", "a") as arquivoBaseTreinamento:
            for texto, usuario in baseTreinamento:
                arquivoBaseTreinamento.write(texto + ',' + usuario)
                arquivoBaseTreinamento.write("\n")

        with open("baseTeste.txt", "a") as arquivoBaseTeste:
            for texto, usuario in baseTeste:
                arquivoBaseTeste.write(texto + ',' + usuario)
                arquivoBaseTeste.write("\n")

    except IOError:
        print('Problemas com na leitura do arquivo')

    arquivoBaseTreinamento.close()
    arquivoBaseTeste.close()


def leituraArquivoBase():
    try:
        with open("base.txt", 'r+') as arquivoLeitura:
            for linha in arquivoLeitura.readlines():
                linha = linha.split(',')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                registro = [texto, usuario]
                if len(basePrincipal) < totalRegistrosPegar:
                    basePrincipal.append(registro)

        escreverArquivos()
    except IOError:
        print('Problemas com na leitura do arquivo')

    arquivoLeitura.close()


if __name__ == "__main__":
    leituraArquivoBase()
