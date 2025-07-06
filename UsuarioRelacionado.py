# Importanto as bibliotecas

import requests
import json
import pandas as pd
import sys

###################################################  ATENCAO  ###################################################
#                                                                                                               #
# Para criar um usuario relacionado, é preciso configurar uma chave de API no modulo A2S do Senha Segura.       #
#                                                                                                               #
#################################################################################################################

# usa o ClientID e ClientSecret para gerar o token e enviar para a variavel result
data = {
    'grant_type': 'client_credentials',
    'client_id': '0000000000',
    'client_secret': '00000000000000000000'
}
response = requests.post('https://[EnderecoDoSenhaSegura]/iso/oauth2/token', data=data)             ##### Alterar o endereço do Senha Segura aqui #####
result = response.json()

response_code = response.status_code
if response_code == 401:
    status_auth = "Não foi possivel autenticar, verifique se o seu endereço de IP esta liberado na aplicação A2A 'Automacao_SI'."
    sys.exit()
elif response_code == 200:
    status_auth = "Autenticação realizada com sucesso. \n"
else:
    status_auth = "Erro não tratado"

print (status_auth)

# Faz uma solictação para receber os usuario relacionados ja existentes no cofre
auth_header = "Bearer " + result['access_token']
headers = {'Authorization': auth_header}
response = requests.get('https://[EnderecoDoSenhaSegura]/iso/user/related', headers=headers)        ##### Alterar o endereço do Senha Segura aqui #####

# converte o resultado em json
response = response.json()
data = json.dumps(response, indent=4)

# converte o Json em Data Frame
tabelaUsers = pd.DataFrame(response['relatedUsers'])

# Testa para saber se o arquivo Excel existe, se não exibe msg de erro e fecha a aplicação
path = 'usuarios_para_relacionar.xlsx'

check_file = os.path.isfile(path)

if check_file == True:
    print("Planilha encontrada, carregando planilha e comparando com os dados existente no Senha Segura")

    # Ler o arquivo Excel com os usuarios para relacionar
    df_excel = pd.read_excel('usuarios_para_relacionar.xlsx')

    # Remover duplicados do Excel com base no JSON, ignorando maiúsculas e minúsculas
    df_result = df_excel[~df_excel[['credencial', 'username']].apply(lambda x: tuple(x.str.lower()), axis=1).isin(tabelaUsers[['name', 'username']].apply(lambda x: tuple(x.str.lower()), axis=1))]

    # Salvar o DataFrame resultante em um novo arquivo Excel, este arquivos contem todos os usuarios/credenciais que a aplicação vai relacionar se não houver erro
    df_result.to_excel('Novos usuários relacionados.xlsx', index=False)

    print("Planilha com novos usuários relacionados criada com sucesso!\n Novos usuários relacionados.xlsx")

else:
    print("Arquivo de excel 'usuarios_para_relacionar.xlsx' não encontrado!")
    sys.exit()



#Loop para criar usaurios relacionados

item = 0

df_result_reset = df_result.reset_index(drop=True)

if df_result_reset.empty:
    print('Não existe usuario novo para relacionar')
else:
    print ("Relacionando usuarios \n")
    for i in df_result_reset.iterrows():
        linha = df_result_reset.loc[item]
        userRelacionado = {
        'name': linha['credencial'],
        'username': linha['username']
    }
        enviado = requests.post('https://[EnderecoDoSenhaSegura]/iso/user/related',headers=headers, data=userRelacionado)       ##### Alterar o endereço do Senha Segura aqui #####
        status_code = enviado.status_code
        if status_code == 400:
            status = "= Usuario (Login) inválido"
        elif status_code == 200:
            status = "= Criado com sucesso"
        else:
            status = "= Erro"
        
        print("Criação do " + linha['username'] +" relacionado com " + linha['credencial'] + " " + status)
        item = item + 1
