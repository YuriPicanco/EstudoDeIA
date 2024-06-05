import os
import json
from manipula_dados import *
from dotenv import load_dotenv
from contador_tokens import calcula_token

load_dotenv()
def analisar_transacao(lista_transacoes):
    print("1. Executando a análise de transação")
    
    model="gpt-4"

    prompt_sistema = """
        Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
        Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

        Cada nova transação deve ser inserida dentro da lista do JSON.

        # Possíveis indicações de fraude
        - Transações com valores muito discrepantes
        - Transações que ocorrem em locais muito distantes um do outro
        
            Adote o formato de resposta abaixo para compor sua resposta.
            
        # Formato Saída 
        {
            "transacoes": [
                {
                "id": "id",
                "tipo": "crédito ou débito",
                "estabelecimento": "nome do estabelecimento",
                "horário": "horário da transação",
                "valor": "R$XX,XX",
                "nome_produto": "nome do produto",
                "localização": "cidade - estado (País)"
                "status": ""
                },
            ]
        } 
    """
    prompt_usuario = f"""Considere o CSV abaixo, onde cada linha é uma transação
                         diferente: {lista_transacoes}. Sua resposta deve adotar 
                         o #Formato de Resposta (apenas um json sem outros comentários)
                      """

    lista_tokens = calcula_token(prompt_sistema+prompt_usuario, model)
   
    lista_mensagens = embalaMensagem(prompt_sistema, prompt_usuario)
    resposta = enviaRequisicaoAoGPT(lista_mensagens).replace("'", '"')
    json_resposta = json.loads(resposta)

    return json_resposta


def gera_alerta(transacao):
    print("2. Gerando parecer para transacao ", transacao["id"])
    prompt_sistema = f"""
                Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
                Transação: {transacao}

                ## Formato de Resposta
                "id": "id",
                "tipo": "crédito ou débito",
                "estabelecimento": "nome do estabelecimento",
                "horario": "horário da transação",
                "valor": "R$XX,XX",
                "nome_produto": "nome do produto",
                "localizacao": "cidade - estado (País)"
                "status": "",
                "parecer" : "Colocar Não Aplicável se o status for Aprovado"
            """

    lista_mensagens = embalaMensagem(prompt_sistema)
    resposta = enviaRequisicaoAoGPT(lista_mensagens)

    print("Finalizando processo de analise")
    return resposta


def gera_recomendacao(parecer):
    print("3. Gerando recomendações")
        
    prompt_sistema = f"""
        Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {parecer}

        As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
        Elas devem ser escritas no formato técnico.

        Inclua também uma classificação do tipo de fraude, se aplicável. 
        """

    lista_mensagens = embalaMensagem(prompt_sistema)
    resposta = enviaRequisicaoAoGPT(lista_mensagens)

    print("Recomendações finalizadas")
    print(resposta)

    return resposta


lista_transacoes = carregaTransacoes()
transacoes_analisadas = analisar_transacao(lista_transacoes)

for transacao in transacoes_analisadas["transacoes"]:
    if transacao["status"] == "Possível Fraude":
        alerta = gera_alerta(transacao)
        recomendacao = gera_recomendacao(alerta)

        alerta_id = transacao["id"]
        alerta_produto = transacao["nome_produto"]
        alert_status = transacao["status"]

        salvaAnalise(f"{alerta_id}-{alerta_produto}-{alert_status}", recomendacao)

