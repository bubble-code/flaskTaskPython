from flask import Flask,jsonify
from flask_cors import CORS
# from Models.Busqueda import Busqueda
from Models.AIQuery import AIQuery


app = Flask(__name__)
CORS(app)
# busqueda_instance = Busqueda()
ai_instalce = AIQuery()
ai_instalce.add_contents()

# @app.route('/api/busqueda')
# def GetBusqueda():
#     open_file = busqueda_instance.OpenFile()
#     col_names = busqueda_instance.names_col_cliente
#     read_ids = busqueda_instance.ReadDataFromExcel(open_file=open_file,name_columns=col_names)
#     result_query = busqueda_instance.HacerBusqueda(list_ids=read_ids)
#     busqueda_instance.GuardarDatos(df_result=result_query)
#     #return result_query.to_json(orient='records')
#     return result_query.to_json(orient='records')


@app.route('/api/ai')
def GetQuestion():
    response = ai_instalce.Hacer_pregunta(prompt="Give me the id of the 5 articulos the type 01")
    # response = ai_instalce.Get_context_data()
    return response

if __name__ == "__main__":
    app.run(debug=True,port=5000)

