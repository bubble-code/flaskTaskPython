import pandas as pd
import pyodbc


class Busqueda:
    def __init__(self):
        self.ruta_file = r"C:\Users\a.obregon\OneDrive - FAVRAM, S.L\Escritorio\Repo\Busqueda1.xlsx"
        self.ruta_file_falta_cliente = r"C:\Users\a.obregon\OneDrive - FAVRAM, S.L\Escritorio\BusquedaFaltaCliente.xlsx"
        self.hoja = "Hoja1"
        self.server = r'SERVIDOR\SOLMICRO6'
        self.database = 'SolmicroERP6_PruebasSub'
        self.names_col = ["Artículo"]
        self.names_col_cliente = ["ID"]
        self.username = 'sa'
        self.password = 'Altai2021'
        self.connection_string = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.conn = self.OpenConnection(self.connection_string)
        self.string_query_mayor04 = "SELECT IDArticulo, DescArticulo, IDContador, FechaAlta, IDEstado, IDTipo, IDFamilia, IDSubfamilia, CCVenta, CCExport, CCCompra, CCImport, CCVentaRegalo, CCGastoRegalo, CCStocks, IDTipoIva, IDPartidaEstadistica, IDUdInterna, IDUdVenta, IDUdCompra, PrecioEstandarA, PrecioEstandarB, FechaEstandar, UdValoracion, PesoNeto, PesoBruto, TipoEstructura, IDTipoEstructura, TipoRuta, IDTipoRuta, CodigoBarras, PuntoVerde, PVPMinimo,PorcentajeRechazo, Plazo, Volumen, RecalcularValoracion, CriterioValoracion, GestionStockPorLotes, PrecioUltimaCompraA, PrecioUltimaCompraB, FechaUltimaCompra, IDProveedorUltimaCompra, LoteMultiplo,CantMinSolicitud, CantMaxSolicitud, LimitarPetDia, IdArticuloConfigurado, ContRadical, IdFamiliaConfiguracion, PrecioBase, Configurable, FechaCreacionAudi, FechaModificacionAudi, UsuarioAudi, NivelPlano, StockNegativo,PlazoFabricacion, ParamMaterial, ParamTerminado, CapacidadDiaria, AplicarLoteMRP, NSerieObligatorio, PuntosMarketing, ValorPuntosMarketing, ValorReposicionA, ValorReposicionB, FechaValorReposicion,ControlRecepcion, IDEstadoHomologacion, IDArticuloFinal, GenerarOFArticuloFinal, IdDocumentoEspecificacion, NivelModificacionPlan, FechaModificacionNivelPlan, TipoFactAlquiler, Seguridad, Reglamentacion,SeguridadReglamentacion, DiasMinimosFactAlquiler, SinDtoEnAlquiler, SinSeguroEnAlquiler, NecesitaOperario, IDConcepto, CCVentaGRUPO, CCExportGRUPO, CCImportGRUPO, CCCompraGRUPO, FacturacionAsociadaMaq,FactTasaResiduos, NoImprimirEnFactura, IDArticuloContenedor, QContenedor, IDArticuloEmbalaje, QEmbalaje, Color, IDCaracteristicaArticulo1, IDCaracteristicaArticulo2, IDCaracteristicaArticulo3, IDCaracteristicaArticulo4,IDCaracteristicaArticulo5, IDArticuloPadre, TipoPrecio, IDTipoProducto, IDTipoMaterial, IDTipoSubMaterial, IDTipoEnvase, IDComerIndus, IDTipoIVAReducido, IDUdInterna2, Observaciones, PorcenIVANoDeducible,PrecioBaseConfigurado, Alias, IDCategoria, IDAnada, IDColorVino, IDCategoriaVino, IDFormato, IDMarcaComercial, IDEmpresa, RetencionIRPF, IncluirEnEMCS, ClaveDeclaracion, IDRegistroFitosanitario, RiquezaNPK,IDTipoAbono, IDTipoFertilizacion, ClaveProductoSilicie, TipoEnvaseSilicie, ExcluirSilicie, IDCalificacion, IDProductoVino, IDPaisOrigen, CodigoEstructura, Certif31, Ubicacion, Codigo3, Descripcion2, INFAPP, EJEN15085,TIPO15085, ExcluirCupos, IDCampanaCupoClasificacion, KGPlastico, KGPlasticoNR, ClaveProducto, GestionContraPedidoVenta, UsuarioCreacionAudi, Espesor FROM tbMaestroArticulo WHERE(IDTipo < N'04')"

    def __del__(self):
        self.CloseConnection()

    def CloseConnection(self):
        try:
            self.conn.close()
        except Exception as e:
            print("Error al cerrar la conexion:", e)

    def OpenFile(self):
        try:
           # df = pd.read_excel(self.ruta_file, sheet_name=self.hoja)
            df = pd.read_excel(self.ruta_file_falta_cliente, sheet_name=self.hoja)
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
            #cursor.execute("Select CodigoArticulo, Descripcion,RevisionPlano,Existencia,FechaUltimaSalida,ProveedorHabitual from MArticulo where CodigoArticulo = ?", id)
            cursor.execute("SELECT IDProveedor FROM tbMaestroProveedor WHERE IDProveedor = ?", id)
            rows = cursor.fetchall()
            if not rows:
                resultado.append([id])
            #for row in rows:
               # resultado.append([row.CodigoArticulo,row.Descripcion,row.RevisionPlano,row.Existencia,row.FechaUltimaSalida,row.ProveedorHabitual])                
        #df_resultados = pd.DataFrame(resultado,columns=["CodigoArticulo","Descripcion","RevisionPlano","Existencia","FechaUltimaSalida","ProveedorHabitual"])
        df_resultados = pd.DataFrame(resultado,columns=["CodigoArticulo"])
        cursor.close()
        return df_resultados
    
    def BusquedaArtVenta(self):
        resultado = []
        cursor = self.conn.cursor()
        cursor.execute(self.string_query_mayor04)
        rows = cursor.fetchall()
        for row in rows:
            resultado.append([row])
        cursor.close()
        return resultado


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
        with pd.ExcelWriter(self.ruta_file_falta_cliente,engine='openpyxl',mode='a') as writer:
            df_result.to_excel(writer,sheet_name='Resultados',index=False)
        print('Proceso terminado')


