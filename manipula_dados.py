import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def carregaAvaliacao(produto):
    caminho_do_arquivo=(f"./dados/avaliacoes-{produto}.txt")
    try:
        with open(caminho_do_arquivo, 'r') as arquivo:
            dados=arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


def carregaAnalise(produto):
    caminho_do_arquivo=(f"./dados/analise-{produto}.txt")
    try:
        with open(caminho_do_arquivo, 'r') as arquivo:
            dados=arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


def carregaTransacoes():
    caminho_do_arquivo=(f"./dados/dadosTransacoes/transacoes.csv")
    try:
        with open(caminho_do_arquivo, 'r') as arquivo:
            dados=arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


def salvaAnalise(produto, conteudo):
    caminho_do_arquivo=(f"./dados/analise-{produto}.txt")
    try:
        with open(caminho_do_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
            print(f"Error ao salvar arquivo: {e}")


def salvaAlerta(produto, conteudo):
    caminho_do_arquivo=(f"./dados/alerta-{produto}.txt")
    try:
        with open(caminho_do_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
            print(f"Error ao salvar arquivo: {e}")


def embalaMensagem(prompt_sistema=None, prompt_usuario=None):
    lista_mensagens = []
    if prompt_sistema:
        lista_mensagens.append({
            "role":"system",
            "content":prompt_sistema
        })
    if prompt_usuario:
        lista_mensagens.append({
            "role":"user",
            "content":prompt_usuario
        })
    return lista_mensagens


def  enviaRequisicaoAoGPT(lista_mensagens, model="gpt-4", temperature = 0):
    try:
        cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        resposta = cliente.chat.completions.create(
            messages = lista_mensagens,
            model = model,
            temperature = temperature
        )

        return resposta.choices[0].message.content
    except OpenAI.AuthenticationError as e:
        print(f"Erro de Autenticação: {e}")
    except OpenAI.APIError as e:
        print(f"Erro de API: {e}")
    