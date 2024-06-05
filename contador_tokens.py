import tiktoken

def gpt_4(message):
    model = "gpt-4"
    condificador = tiktoken.encoding_for_model(model)
    lista_tokens = condificador.encode(message)
    numero_tokens = len(lista_tokens)
    
    print("Modelo:", model)
    # print("Lista de Tokens: ", lista_tokens)
    print("Total de tokens:", len(lista_tokens))
    print(f"Custo para o modelo {model} é de ${(len(lista_tokens)/1000)*0.03}")

    return lista_tokens

def gpt_35_turbo(message):
    model = "gpt-3.5-turbo"
    condificador = tiktoken.encoding_for_model(model)
    lista_tokens = condificador.encode(message)
    
    print("Modelo:", model)
    # print("Lista de Tokens: ", lista_tokens)
    print("Total de tokens:", len(lista_tokens))
    print(f"Custo para o modelo {model} é de ${(len(lista_tokens)/1000)*0.03}")

    return lista_tokens

cases = {
    "gpt-4": gpt_4,
    "gpt-3.5-turbo": gpt_35_turbo
}

def calcula_token(message, model):
    case_function = cases.get(model)
    
    if case_function:
        return case_function(message)
    else:
        print("Modelo inválido")
