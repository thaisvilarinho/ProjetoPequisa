# -*- coding: utf-8 -*-

# Importar bibliotecas
import tweepy as tw
import TwitterCredentials as credenciais
import pymysql
from pymysql import ProgrammingError


def obter_tweets(usuario, api, cursor):

    # Busca tweets de um usuário específico em sua timeline, exluindo retweets
    resultado = tw.Cursor(api.user_timeline, screen_name=usuario,
                          include_rts='false', tweet_mode="extended").items()
    tweets = []

    # Pecorre a timeline do usuário pegando de 20 em 20 tweets
    for r in resultado:
        id_str = r.id_str
        created = r.created_at
        text = r.full_text
        name = r.user.screen_name

        tweets.append(text)
        print("...%s total de tweets carregados" % (len(tweets)))

        try:
            comando_sql = "INSERT INTO tweets(id_str, created, text, name) " \
                          "VALUES (%s, %s, %s, %s)"
            valor = [(id_str, created, text, name)]
            cursor.executemany(comando_sql, valor)
            conexao.commit()

        except ProgrammingError as err:
            print(err)

    return tweets


if __name__ == '__main__':
    # Autenticação API tweepy
    auth = tw.OAuthHandler(credenciais.CONSUMER_KEY, credenciais.CONSUMER_SECRET)
    auth.set_access_token(credenciais.ACESS_TOKEN, credenciais.ACESS_TOKEN_SECRET)

    # Gera interface de autenticação com o twitter
    api = tw.API(auth)

    # Usuário que será buscados os tweets
    usuario = 'xxx'

    # Conexão com o banco de dados
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='Twitter')

    # Comando que executar as instruções
    cursor = conexao.cursor()

    # Filtrar os tweets de um usuário específico
    tweets = obter_tweets(usuario, api, cursor)

    conexao.close()
    cursor.close()
