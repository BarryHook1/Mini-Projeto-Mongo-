# Chat Criptografado com AES e MongoDB

Este é um programa de chat simples que usa criptografia AES (AES-PKCS5) para proteger mensagens enviadas entre usuários. As mensagens são armazenadas em um banco de dados MongoDB e podem ser descriptografadas apenas pelo destinatário correto, usando uma chave de criptografia compartilhada.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados em seu ambiente de desenvolvimento:

- Python 3.x
- MongoDB
- Pacotes Python necessários (instalados no ambiente virtual):
  - `pymongo`
  - `pycryptodome`
  
## Instalação

1. Clone este repositório para o seu ambiente local:
   ```bash
   git clone https://github.com/BarryHook1/Mini-Projeto-Mongo-.git
   ``` 
2. Crie um ambiente virtual e ative-o:
   ### No Windows:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```
    ### No Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. Instale as dependências necessárias:
 ```bash
pip install -r requirements.txt
 ```
## Configuração
- Verifique se o MongoDB está rodando localmente ou em um servidor remoto.
- Configure a conexão com o MongoDB no arquivo mongohandler.py, substituindo a URI do MongoDB se necessário.

# Importante 
- A chave de criptografia para todos os usuários no exemplo é a2b3. Esta chave deve ser compartilhada entre os usuários para que as mensagens possam ser descriptografadas corretamente.
- O salt exclusivo de cada usuário é usado para garantir a segurança da chave gerada.
