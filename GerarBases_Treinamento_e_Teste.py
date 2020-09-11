# -*- coding: utf-8 -*-
from sklearn.model_selection import train_test_split

basePrincipal = []
baseTreinamento = []
baseTeste = []
totalRegistrosPegar = 0
PorcentagemBaseTeste = 0.2


def escreverArquivos():
    baseTreinamento, baseTeste = train_test_split(basePrincipal, test_size=PorcentagemBaseTeste)

    print("Tamanho base principal: ", len(basePrincipal))
    print("Tamanho base treinamento: ", len(baseTreinamento))
    print("Tamanho base teste: ", len(baseTeste))

    try:
        with open("baseTreinamento.txt", "a", encoding="utf-8") as arquivoBaseTreinamento:
            for texto, usuario in baseTreinamento:
                arquivoBaseTreinamento.write(texto + '#' + usuario)
                arquivoBaseTreinamento.write("\n")

        with open("baseTeste.txt", "a", encoding="utf-8") as arquivoBaseTeste:
            for texto, usuario in baseTeste:
                arquivoBaseTeste.write(texto + '#' + usuario)
                arquivoBaseTeste.write("\n")

    except IOError:
        print('Problemas com na leitura do arquivo')

    arquivoBaseTreinamento.close()
    arquivoBaseTeste.close()


def leituraArquivoBase():
    try:
        with open("base.txt", 'r+', encoding="utf-8") as arquivoLeitura:
            for linha in arquivoLeitura:
                linha = linha.split('#')
                linha = [x.strip() for x in linha]
                texto = linha[0]
                usuario = linha[1]
                if len(texto) > 0:
                    registro = [texto, usuario]
                    if len(basePrincipal) < totalRegistrosPegar:
                        basePrincipal.append(registro)

        escreverArquivos()
    except IOError:
        print('Problemas com na leitura do arquivo')

    arquivoLeitura.close()


if __name__ == "__main__":
    leituraArquivoBase()
