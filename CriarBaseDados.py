# -*- coding: utf-8 -*-

# Importar bibliotecas
import pymysql
from mysql.connector import Error


def criarBaseDeDados(nomeBaseDeDados):
    # Conexão com o banco de dados
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='')

    # Comando que executar as instruções
    cursor = conexao.cursor()

    try:
        # Cria o banco de dados
        cursor.execute("CREATE DATABASE " + nomeBaseDeDados + " CHARSET = utf8 COLLATE = utf8_general_ci")
    except Error as e:
        print("Erro ao gerar a base de dados " + nomeBaseDeDados + " no MYSQL", e)

    cursor.close()
    conexao.close()


def criarTabela(nomeBaseDeDados, nomeTabela):
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database=nomeBaseDeDados
    )
    # Comando que executar as instruções
    cursor = conexao.cursor()

    try:
        # Criando as tabelas no banco de dados
        cursor.execute("CREATE TABLE IF NOT EXISTS " + nomeTabela + "(id_str VARCHAR(255) PRIMARY KEY, "
                                                                    "created TIMESTAMP, text LONGTEXT CHARACTER "
                                                                    "SET utf8mb4 COLLATE utf8mb4_unicode_ci, "
                                                                    "name VARCHAR(255))")

    except Error as e:
        print("Erro ao gerar a tabela " + nomeTabela + " na base de dados" + nomeBaseDeDados, e)

    conexao.close()
    cursor.close()


if __name__ == '__main__':
    nomeBaseDeDados = 'TwitterD'
    nomeTabela = 'tweets'
    criarBaseDeDados(nomeBaseDeDados)
    criarTabela(nomeBaseDeDados, nomeTabela)
