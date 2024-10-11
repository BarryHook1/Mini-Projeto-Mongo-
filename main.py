import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from database.mongohandler import MongoHandler
from database.entities import User, ChatMessage
from Crypto.Protocol.KDF import PBKDF2 

debug = 0

# Função auxiliar para exibir mensagens de depuração, se debug estiver ativado
def debug_log(message: str):
    if debug == 1:
        print(message)

# Função de criptografia AES-PKCS5
# Esta função usa uma chave para criptografar a mensagem fornecida, utilizando o modo CBC do AES
def aes_encrypt(message: str, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC)  # Cria uma nova instância do AES no modo CBC
    iv = cipher.iv  # Obtém o vetor de inicialização (IV) gerado automaticamente
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))  # Criptografa a mensagem após adicionar o padding
    debug_log(f"[DEBUG] Vetor de inicialização (IV) gerado: {iv.hex()}")
    debug_log(f"[DEBUG] Mensagem criptografada: {encrypted_message.hex()}")
    return iv + encrypted_message  # Retorna o IV concatenado com a mensagem criptografada

# Função de descriptografia AES-PKCS5
# Esta função descriptografa a mensagem criptografada, utilizando a chave e o IV armazenados
def aes_decrypt(encrypted_message: bytes, key: bytes) -> str:
    iv = encrypted_message[:16]  # Extrai os primeiros 16 bytes como o vetor de inicialização (IV)
    debug_log(f"[DEBUG] Vetor de inicialização (IV) extraído: {iv.hex()}")
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Cria uma instância do AES para descriptografar, utilizando o IV extraído
    decrypted_message = unpad(cipher.decrypt(encrypted_message[16:]), AES.block_size)  # Descriptografa a mensagem e remove o padding
    debug_log(f"[DEBUG] Mensagem descriptografada: {decrypted_message}")
    return decrypted_message.decode()

# Função para gerar uma chave a partir de uma senha utilizando PBKDF2 (Password-Based Key Derivation Function 2)
# O salt do usuário é utilizado para garantir que a chave gerada seja única
def generate_key(password: str, user_salt: bytes) -> bytes:
    password = password.encode('utf-8')  # Converte a senha para bytes
    key = PBKDF2(password, user_salt, dkLen=32, count=1000)  # Gera uma chave de 32 bytes usando PBKDF2
    debug_log(f"[DEBUG] Gerando chave com salt: {user_salt.hex()}")
    debug_log(f"[DEBUG] Chave derivada: {key.hex()}")
    return key

# Função para enviar uma mensagem criptografada de um usuário (sender) para outro (receiver)
def send_message(mongo_handler, sender: str, receiver: str):
    message = input("Digite sua mensagem: ")  # Solicita a mensagem a ser enviada
    password = getpass.getpass("Digite a chave de encriptação: ")  # Solicita a senha de criptografia do remetente

    user = mongo_handler.find_user(sender)  # Busca o registro do usuário (remetente) no banco de dados
    key = generate_key(password, user['salt'])  # Gera a chave de criptografia usando a senha e o salt do remetente
    
    encrypted_message = aes_encrypt(message, key)  # Criptografa a mensagem usando a chave gerada
    chat_message = ChatMessage(sender, receiver, encrypted_message)  # Cria um objeto de mensagem de chat com a mensagem criptografada
    mongo_handler.insert_message(chat_message)  # Insere a mensagem criptografada no banco de dados
    
    print("Mensagem enviada com sucesso!")  # Exibe confirmação de que a mensagem foi enviada

# Função para ler e descriptografar as mensagens recebidas por um usuário
def read_messages(mongo_handler, user: str):
    password = getpass.getpass("Digite a chave de encriptação: ")  # Solicita a senha para descriptografar as mensagens

    messages = mongo_handler.find_messages(user)  # Busca as mensagens destinadas ao usuário no banco de dados
    for msg in messages:
        try:
            sender = msg['sender']  # Obtém o remetente da mensagem
            sender_record = mongo_handler.find_user(sender)  # Busca o salt do remetente no banco de dados
            sender_salt = sender_record['salt']
            
            debug_log(f"[DEBUG] Salt do remetente {sender}: {sender_salt.hex()}")

            # Gera a chave de descriptografia com base no salt do remetente e na senha fornecida
            key = generate_key(password, sender_salt)

            # Descriptografa a mensagem
            encrypted_message = msg['message']
            decrypted_message = aes_decrypt(encrypted_message, key)
            print(f"From {msg['sender']}: {decrypted_message}")
        
        except Exception as e:
            print(f"Falha ao decriptar a mensagem de {msg['sender']} (chave errada?).")
            continue  # Continua para a próxima mensagem, mesmo em caso de erro

def main():
    mongo_handler = MongoHandler()  # Inicializa o mongohandler

    user = input("Insira o userID (Alice/Bob): ")  # Solicita o ID do usuário
    action = input("Mandar ou Ler mensagens? (mandar/ler): ").lower()  # Solicita a ação que o usuário deseja realizar

    if action == 'mandar':
        receiver = input("userId do destinatário: ")  # Solicita o ID do destinatário
        send_message(mongo_handler, user, receiver)  # Chama a função para enviar a mensagem
    elif action == 'ler':
        read_messages(mongo_handler, user)  # Chama a função para ler as mensagens
    else:
        print("Tente novamente ( mandar ou ler ) ")  # Exibe uma mensagem de erro se a ação for inválida

if __name__ == "__main__":
    main()
