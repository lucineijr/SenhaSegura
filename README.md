Aplicação para Relacionamento de Usuário e Credencial no Senha Segura
Esta aplicação é usada para relacionar usuários a credenciais.
  Usuário: conta utilizada por uma pessoa para logar na ferramenta.
  Credencial: conta que a ferramenta gerencia e faz o rotacionamento de senha.

Dependências
É necessário instalar duas bibliotecas no Python para que a aplicação rode:  
- pandas  
- requests

Você pode instalá-las executando o comando:  
- pip install requests pandas



Configuração no Senha Segura
No lado do Senha Segura, será necessário:
Criar uma chave de API no módulo A2A.
Alterar o Client_ID e Client_Secret na aplicação conforme os dados fornecidos pelo Senha Segura.
Alterar o endereço do Senha Segura de acordo com o seu ambiente
  
Entrada de Dados
A lista de usuários e credenciais deve estar em um arquivo .xlsx (nome: "usuarios_para_relacionar.xlsx") com apenas duas colunas:  
Coluna A (A1 = username): insira os usuários  
Coluna B (B1 = credencial): insira as credenciais que deseja relacionar ao usuário da coluna A


  
Exemplo:

|username | credencial |
|---------|------------|
|user1 | CredencialA |
|user1 | CredencialB |
|user1 | CredencialC |
|user2 | CredencialA |
|user3 | CredencialB |

    
Execução e Resultados
Após rodar a aplicação:

Será gerado um novo arquivo "Novos usuários relacionados.xlsx"  com os usuários/credenciais que foram criados com sucesso.
O status da criação de cada usuário relacionado pode ser acompanhado pelo console do Python.
