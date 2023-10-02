import openai
import json
import spacy


class AIQuery:
    def __init__(self):
        self.ruta_file = r"C:\Users\a.obregon\source\repos\flaskTaskPython\Models\estructura_tablas.json"
        # openai.api_key = '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'
        # openai.api_key = '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'
        self.context = [{
            'role': 'system',
            'content': """you are a bot to assist in create SQL commands, all your answers should start with \
                this is your SQL, and after that an SQL that can do what the user request.\
                    Your Database is composed by a SQL database with some tables. \
                        Try to Maintain the SQL order simple. Put the SQL command in white letters with a black background, and just after \
                            a simple and concise text explaining how it works. If the user ask for something that can not be solved with an SQL Order \
                                just answer something nice and simple and ask him for something that \
                                    can be solved with SQL.
                                    """
        }]
        self.nlp = spacy.load('es_core_news_sm')

    def identificar_tablas_objetivo(self, pregunta):
        doc = self.nlp(pregunta)
        tablas_coincidentes = []
        for ent in doc.ents:
            ent_text = ent.text.lower()
            for nombre_tabla in nombres_tablas:
                nombre_tabla = nombre_tabla.lower()
            if nombre_tabla in ent_text:
                tablas_coincidentes.append(nombre_tabla)
                if tablas_coincidentes:
                    return tablas_coincidentes
                else:
                    return None

    def Get_context_data(self):
        try:
            with open(self.ruta_file, "r") as file:
                return json.load(file)
                # return self.estructure_db
        except Exception as e:
            print("Error al cargar", e)
            exit(1)

    def add_contents(self):
        json_data = self.Get_context_data()
        contents = json_data["content"]
        for content in contents:
            table_name = content["tableName"]
            self.context.append(
                {'role': 'system', 'content': f"{table_name}:{json.dumps(content)}"})
        # print(self.context)

    def Hacer_pregunta(self, prompt, max_tokens=100, temperature=0.5, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]):
        # self.context.append( {'role':'system', 'content':"""first table: { "tableName": "employees", "fields": [ { "nombre": "ID_usr", "tipo": "int" }, { "nombre": "name", "tipo": "string" }]}"""})
        # self.context.append( {'role':'system', 'content':"""second table:{"tableName": "salary","fields":[{"nombre": "ID_usr","type": "int"},{"name": "year","type": "date"},{"name": "salary","type": "float"}]}"""})
        # self.context.append( {'role':'system', 'content':"""third table:{"tablename": "studies","fields": [{"name": "ID","type": "int"},{"name": "ID_usr","type": "int"},{"name": "educational level","type": "int"},{"name": "Institution","type": "string"},{"name": "Years","type": "date"}{"name": "Speciality","type": "string"}]}"""})
        # self.context.append(self.Get_context_data())
        self.context.append({'role': 'user', 'content': f"{prompt}."})
        # self.context.append({'role': 'system', 'content': r"Remember your instructions as SQL Assistant."})
        # print(self.context)
        openai.api_key = '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'
        # openai.api_key = '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'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context,
            max_tokens=max_tokens,
            temperature=temperature,
            # top_p=top_p,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
            # stop=stop,

        )
        self.context.append({'role': 'assistant', 'content': f"{response}"})
        message = response.choices[0].message.content
        index_inicio = message.upper().index("SELECT")
        index_final = message.index(';')
        sql = response.choices[0].message.content[index_inicio:index_final]
        return sql
