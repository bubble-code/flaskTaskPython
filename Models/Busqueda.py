import pandas as pd
import pyodbc


class Busqueda:
    def __init__(self):
        self.ruta_file = r"C:\Users\a.obregon\OneDrive - FAVRAM, S.L\Escritorio\Repo\Busqueda1.xlsx"
        self.hoja = "Hoja1"
        self.server = r'SERVIDOR'
        self.database = 'IPFavram'
        self.names_col = ["Artículo"]
        self.username = 'sa'
        self.password = '71zl6p9h'
        self.connection_string = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.conn = self.OpenConnection(self.connection_string)

    def __del__(self):
        self.CloseConnection()

    def CloseConnection(self):
        try:
            self.conn.close()
        except Exception as e:
            print("Error al cerrar la conexion:", e)

    def OpenFile(self):
        try:
            df = pd.read_excel(self.ruta_file, sheet_name=self.hoja)
            return df
        except Exception as e:
            print("Error al cargar", e)
            exit(1)

    def OpenConnection(self,connection_string):
        try:
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            print("Error", e)
            exit(1)

    def HacerBusqueda(self, list_ids):
        resultado = []
        cursor = self.conn.cursor()
        for id in list_ids:
            cursor.execute(
                "Select CodigoArticulo, Descripcion,RevisionPlano,Existencia,FechaUltimaSalida,ProveedorHabitual from MArticulo where CodigoArticulo = ?", id)
            rows = cursor.fetchall()
            for row in rows:
                resultado.append([row.CodigoArticulo,row.Descripcion,row.RevisionPlano,row.Existencia,row.FechaUltimaSalida,row.ProveedorHabitual])                
        df_resultados = pd.DataFrame(resultado,columns=["CodigoArticulo","Descripcion","RevisionPlano","Existencia","FechaUltimaSalida","ProveedorHabitual"])
        cursor.close()
        return df_resultados

    def ReadDataFromExcel(self,open_file,name_columns):
        df = open_file
        id_articulos = df[name_columns[0]].tolist()
        return id_articulos

    def FormatData(self,query_data):
        resultado = []
        id_articulos = self.ReadDataFromExcel()
        for id in id_articulos:
            resultado.append([id])
        df_resultados = pd.DataFrame(resultado, columns=["CodigoArticulos"])
        return df_resultados
    
    def GuardarDatos(self,df_result):
        with pd.ExcelWriter(self.ruta_file,engine='openpyxl',mode='a') as writer:
            df_result.to_excel(writer,sheet_name='Resultados',index=False)
        print('Proceso terminado')


