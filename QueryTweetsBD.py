# -*- coding: utf-8 -*-

# Importar bibliotecas
import re
import mysql.connector
from mysql.connector import Error


# Expressão regular remove nome de usuários mencionados nos tweets, hyperlinks e espaços desnecessários

def preprocessamento(texto):

    texto = re.sub(r'@(\w+)', ' ', texto)
    texto = re.sub(r'#(\w+)', ' ', texto)
    texto = re.sub(r'(http\S+)', ' ', texto)
    texto = re.sub(r'[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\-|().:;,!?/{}\]\[\\ ]', '', texto)
    texto = re.sub("\s+", ' ', texto)
    texto = re.sub(r' +', ' ', texto)
    return texto


def pegarDadosTweet(conexao):
    cursor = conexao.cursor()
    try:
        query = "select text, name from " + tabela
        cursor.execute(query)
        tweets = cursor.fetchall()
        print("Total linhas resultado da consulta: ", cursor.rowcount)

        with open('base.txt', 'a', encoding="utf-8") as arquivo:
            for texto, usuario in tweets:
                texto = preprocessamento(texto)
                texto = texto.strip()
                registro = texto + "#" + usuario
                if len(texto) > 0 and registro not in basePrincipal:
                    arquivo.write(registro)
                    arquivo.write("\n")
                    basePrincipal.append(registro)
    except Error as e:
        print("Erro ao acessar dados da tabela 'tweets' no banco de dados", e)
    finally:
        if conexao.is_connected():
            conexao.close()
            cursor.close()
            arquivo.close()
            print("Total de registros extraídos: ", str(len(basePrincipal)))
            print("conexão com MySQL foi finalizada")


if __name__ == "__main__":
    basePrincipal = []
    baseDeDados = "Twitter"
    tabela = 'tweets'

    conexao = mysql.connector.connect(host='localhost', user='root', passwd='', database=baseDeDados)
    pegarDadosTweet(conexao)
