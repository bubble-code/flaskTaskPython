
class ObtEstrucDB:
    def __init__(self):
        self.server = r'SERVIDOR\SOLMICRO6'
        self.database = 'SolmicroERP6_PruebasSub'
        self.names_col = ["Artículo"]
        self.names_col_cliente = ["ID"]
        self.username = 'sa'
        self.password = 'Altai2021'
        self.connection_string = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.conn = self.OpenConnection(self.connection_string)

    def GetEstrucura(self):
        tables_query =[]
        string_query= "Select * from db"