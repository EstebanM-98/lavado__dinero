import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from mysql.connector import Error
from loggs import logs
import os

class SQLtools:

    def __init__(self,params):

        self.user = params['user']
        self.password = params['password']
        self.database = params['database']
        self.host = params['host']
        self.raise_on_warnings = params['raise_on_warnings']
        self.conn = mysql.connector.connect(**params)
        self.log_reg = logs(os.path.join(os.getcwd(),'scripts','read','logs','logs.log'))
        # Crear una conexión SQLAlchemy
        self.engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}")
        try: 
            if self.conn.is_connected():
                print('Conexión establecida con éxito.') 
                self.log_reg.info('Conexión establecida con MySQL')

        except mysql.connector.Error as err:
            print(f'Error al conectar a la base de datos: {err}')
            self.log_reg.error(f'Error en establecer conexion: {err}' )

    def create_table(self):

        cursor = self.conn.cursor(buffered=True)

        try:
            # Dropping table iris if exists
            print('Iniciando creación de tabla Dataorigin')
            self.log_reg.info('Iniciando creación de tabla Dataorigin')
            cursor.execute("DROP TABLE IF EXISTS Dataorigin")
            sql = '''CREATE TABLE Dataorigin (
                Time TIMESTAMP NOT NULL,
                From_Bank INT NOT NULL,
                Account VARCHAR(255) NOT NULL,
                To_Bank INT NOT NULL,
                Account2 VARCHAR(255) NOT NULL,
                Amount_Received DOUBLE NOT NULL,
                Receiving_Currency VARCHAR(255) NOT NULL,
                Amount_Paid DOUBLE NOT NULL,
                Payment_Currency VARCHAR(255) NOT NULL,
                Payment_Format VARCHAR(255) NOT NULL,
                Is_Laundering INT NOT NULL
            )'''

            # Creating a table
            cursor.execute(sql);
            print("Creacion de tabla exitosa................")
            self.log_reg.info("Creacion de tabla exitosa................")
        except Exception as err:
            print("Error en la creacion de la tabla Dataorigin", err)    
            self.log_reg.error(f"Error en la creacion de la tabla Dataorigin: {err}")


    # Define function using cursor.executemany() to insert the dataframe
    def execute_many(self,path):
        
        datafrm = pd.read_csv(path)
        
        datafrm['Time'] = datafrm['Time'].str.replace('/', '-')
        # Creating a list of tupples from the dataframe values
        tpls = [tuple(x) for x in datafrm.to_numpy()]
            
        cols = ','.join(list(datafrm.columns))

        sql = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % ('Dataorigin', cols)
        
        x = 1000000

        try:

            for i in range(0,len(tpls),x):

                cursor = self.conn.cursor()
                cursor.executemany(sql, tpls[i:i+x])
                self.conn.commit()
                cursor.close()

            print("Los datos han sido insertados correctamente")
            self.log_reg.info("Los datos han sido insertados correctamente")
            
        except Exception as e:
            print(f"Error insertando los datos: {e}")
            self.log_reg.error(f"Error insertando los datos: {e}")
            cursor.close()
        
    def getSql(self,path):

        with open(path, "r") as file:
            sql_code = file.read()
                # Elimina los saltos de línea del código SQL
        sql_code = sql_code.replace('\n',' ')

        # Divide el código SQL en instrucciones individuales basadas en el punto y coma
        sql_statements = sql_code.split(';')

        # Elimina los espacios en blanco alrededor de cada instrucción y cualquier instrucción vacía
        sql_statements = [statement.strip() for statement in sql_statements if statement.strip()]

        return sql_statements

    def executeSql(self,querie):

        try:
            print(f'Ejecutando querie: {querie}')
            self.log_reg.info(f'Ejecutando querie: {querie}')
            cursor = self.conn.cursor(buffered=True)
            cursor.execute(querie)
        except Exception as e:
            print(f'La ejecución del querie fallo: {e}')
            self.log_reg.error(f"Error insertando los datos: {e}")
        #self.conn.commit()
        #cursor.close()

    def getDisconnected(self):

        print('Cerrando conexion')
        self.log_reg.info('Cerrando conexion')
        self.conn.close()
        self.engine.dispose()