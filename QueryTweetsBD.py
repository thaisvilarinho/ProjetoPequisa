# -*- coding: utf-8 -*-

# Importar bibliotecas
import mysql.connector
from mysql.connector import Error
import numpy as np


try:
    connection = mysql.connector.connect(host='localhost', user='root', passwd='', database='Twitter')

    query = "select text, name from tweets"
    cursor = connection.cursor()
    cursor.execute(query)
    tweets = cursor.fetchall()
    print("Total linhas resultado da consulta: ", cursor.rowcount)

    with open('base.txt', 'a') as arquivo:
        for texto, usuario in tweets:
            if texto != '':
                arquivo.write(texto + ',' + usuario)
                arquivo.write("\n")

except Error as e:
    print("Erro ao acessar dados da tabela 'tweets' no banco de dados", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("conexão com MySQL foi finalizada")


arquivo.close()