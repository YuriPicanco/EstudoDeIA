from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def Modelo_gpt_4(nome_produto, lista_categorias_possiveis):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-3.5-turbo-16k"

    prompt_sistema = f"""
            Você é um categorizador de produtos.
            Você deve assumir as categorias presentes na lista abaixo.

            # Lista de Categorias Válidas
            {lista_categorias_possiveis.split(",")}

            # Formato da Saída
            Produto: Nome do Produto
            Categoria: apresente a categoria do produto

            # Exemplo de Saída
            Produto: Escova elétrica com recarga solar
            Categoria: Eletrônicos Verdes
        """

    prompt_usuario = nome_produto

    numero_tokens = calcula_token(message=prompt_sistema + prompt_sistema)

    if(numero_tokens > 2048):
        model="gpt-4"

    lista_mensagens = [
            {"role":"system","content": prompt_sistema},
            {"role":"user","content":prompt_usuario}
            ]

    resposta = client.chat.completions.create(
        messages=lista_mensagens,
        model=model,
        temperature=0,
        max_tokens=200,
    )
    print("Modelo:", model)
    print(resposta.choices[0].message.content)

while True:
    nome_produto = input("Digite o nome do produto: ")
    lista_categorias_possiveis = input("Digite o nome das possíveis categorias, separando por vírgula")

    Modelo_gpt_4(nome_produto, lista_categorias_possiveis)
   


