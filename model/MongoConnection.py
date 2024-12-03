from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# No processo de fazer o deploy no render, o mongoDB Atlas não aceitou a string de conexão com o banco de dados abaixo:
# 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
# Ele recomendou a string de conexão abaixo:
# 'mongodb://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'

class MongoBiomassaConnection:
    def __init__(self) -> None:
        self.__connection_string = (
            'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
        ).format(
            os.getenv("USERNAME"),
            os.getenv("PASSWORD"),
            os.getenv("MONGO_CLUSTER_URL"),
            os.getenv("DATABASE_NAME"),
            os.getenv("MONGO_APP_NAME")
        )
        self.__database_name = os.getenv("DATABASE_NAME")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[self.__database_name]
            print("Conexão bem-sucedida ao MongoDB Biomassa!")
        except ConnectionError as e:
            print("Erro ao conectar ao MongoDB Biomassa:", e)

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client

    def close_connection(self):
        if self.__client is not None:
            self.__client.close()  # Fecha a conexão com o MongoDB
            print("Conexão com o MongoDB, Banco de Dados Biomassa fechada.")

class MongoSolarConnection:
    def __init__(self) -> None:
        self.__connection_string = (
            'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
        ).format(
            os.getenv("USERNAME_2"),
            os.getenv("PASSWORD_2"),
            os.getenv("MONGO_CLUSTER_URL_2"),
            os.getenv("DATABASE_NAME_2"),
            os.getenv("MONGO_APP_NAME_2")
        )
        self.__database_name = os.getenv("DATABASE_NAME_2")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[self.__database_name]
            print("Conexão bem-sucedida ao MongoDB Solar!")
        except ConnectionError as e:
            print("Erro ao conectar ao MongoDB Solar:", e)

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client

    def close_connection(self):
        if self.__client is not None:
            self.__client.close()  # Fecha a conexão com o MongoDB
            print("Conexão com o MongoDB, Banco de Dados Solar fechada.")

class MongoHidroConnection:
    def __init__(self) -> None:
        self.__connection_string = (
            'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
        ).format(
            os.getenv("USERNAME_3"),
            os.getenv("PASSWORD_3"),
            os.getenv("MONGO_CLUSTER_URL_3"),
            os.getenv("DATABASE_NAME_3"),
            os.getenv("MONGO_APP_NAME_3")
        )
        self.__database_name = os.getenv("DATABASE_NAME_3")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[self.__database_name]
            print("Conexão bem-sucedida ao MongoDB Hidrelétricas!")
        except ConnectionError as e:
            print("Erro ao conectar ao MongoDB Hidrelétrica:", e)

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client

    def close_connection(self):
        if self.__client is not None:
            self.__client.close()  # Fecha a conexão com o MongoDB
            print("Conexão com o MongoDB, Banco de Dados Hidrelétricas fechada.")


# Testando a Conexão com o MongoDB Atlas -------------------------------------------------------------------------------
# if __name__ == '__main__':
#
#     # Conexão com o banco de dados Biomassa
#     connection_eolicas = MongoBiomassaConnection()
#     connection_eolicas.connect_to_db()
#     connection_eolicas.close_connection()
#
#     # Conexão com o banco de dados Solar
#     connection_solar = MongoSolarConnection()
#     connection_solar.connect_to_db()
#     connection_solar.close_connection()
#
#     # Conexão com o banco de dados Hidrelétricas
#     connection_hidro = MongoHidroConnection()
#     connection_hidro.connect_to_db()
#     connection_hidro.close_connection()
