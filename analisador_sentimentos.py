import os
from openai import OpenAI
from dotenv import load_dotenv
from manipula_dados import *
from contador_tokens import calcula_token



load_dotenv()

def analisador_sentimentos(produto):
    model="gpt-4"
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """
    prompt_usuario = carregaAvaliacao(produto)

    lista_mensagens = embalaMensagem(prompt_sistema, prompt_usuario)
    lista_tokens = calcula_token(prompt_sistema+prompt_usuario, model)
    if(len(lista_tokens)>2046):
        model="gpt-3.5-turbo"
    print("Iniciando analise do produto")

    resposta = enviaRequisicaoAoGPT(lista_mensagens, model)

    salvaAnalise(produto, resposta)
    print(f"{carregaAnalise(produto)}")

produto = input("Informe um produtor para obter o resumo das avaliações: ")

analisador_sentimentos(produto)