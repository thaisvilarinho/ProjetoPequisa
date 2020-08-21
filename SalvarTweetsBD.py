# -*- coding: utf-8 -*-

# Importar bibliotecas
import tweepy as tw
import re
import TwitterCredentials as credenciais
import pymysql
from pymysql import ProgrammingError


def obter_tweets(usuario, api, cursor):
    # Busca tweets de um usuário específico em sua timeline, exluindo retweets
    resultado = tw.Cursor(api.user_timeline, screen_name=usuario,
                          include_rts='false', tweet_mode="extended").items()
    # Lista que irá receber os textos tratados (sem caracteres especiais e acentuações)
    tweets = []
    # Pecorre a timeline do usuário pegando de 20 em 20 tweets
    for r in resultado:
        id_str = r.id_str
        created = r.created_at
        text = r.full_text
        fav = r.favorite_count
        name = r.user.screen_name
        description = re.sub('[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]', '', r.user.description)
        loc = re.sub('[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]', '', r.user.location)
        user_created = r.user.created_at
        followers = r.user.followers_count

        # Expressão regular caracteres especiais e hyperlinks
        texto_tratado = re.sub(r'@(\w+)|(R\$)|[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ!?;,. ]|(http\S+)', ' ', text)
        tweets.append(texto_tratado)
        print("...%s total de tweets carregados" % (len(tweets)))

        try:
            comando_sql = "INSERT INTO tweets(id_str, created, text, fav, name, description,"\
                          "loc, user_created, followers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valor = [(id_str, created, texto_tratado, fav, name, description, loc, user_created, followers)]
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

    #Conexão com o banco de dados
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='TwitterZ'
    )

    # Comando que executar as instruções
    cursor = conexao.cursor()

    # Filtrar os tweets de um usuário específico
    tweets = obter_tweets(usuario, api, cursor)

    conexao.close()
    cursor.close()

