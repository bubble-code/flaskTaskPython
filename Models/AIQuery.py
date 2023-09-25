import openai

class AIQuery:
    def __init__(self):
        openai.api_key = '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'
        self.context = [ {
            'role':'system', 
            'content':"""you are a bot to assist in create SQL commands, all your answers should start with \
                this is your SQL, and after that an SQL that can do what the user request.\
                    Your Database is composed by a SQL database with some tables. \
                        Try to Maintain the SQL order simple. Put the SQL command in white letters with a black background, and just after \
                            a simple and concise text explaining how it works. If the user ask for something that can not be solved with an SQL Order \
                                just answer something nice and simple and ask him for something that \
                                    can be solved with SQL.
                                    """
                                    } ]
         
    def Hacer_pregunta(self,prompt,max_tokens=100,temperature=0.5,top_p=1.0, frequency_penalty=0.0,presence_penalty=0.0, stop=["\n"]):
        self.context.append( {'role':'system', 'content':"""first table: { "tableName": "employees", "fields": [ { "nombre": "ID_usr", "tipo": "int" }, { "nombre": "name", "tipo": "string" }]}"""})
        self.context.append( {'role':'system', 'content':"""second table:{"tableName": "salary","fields":[{"nombre": "ID_usr","type": "int"},{"name": "year","type": "date"},{"name": "salary","type": "float"}]}"""})
        self.context.append( {'role':'system', 'content':"""third table:{"tablename": "studies","fields": [{"name": "ID","type": "int"},{"name": "ID_usr","type": "int"},{"name": "educational level","type": "int"},{"name": "Institution","type": "string"},{"name": "Years","type": "date"}{"name": "Speciality","type": "string"}]}"""})
        self.context.append({'role':'user', 'content':f"{prompt}."})
        self.context.append({'role':'system', 'content':r"Remember your instructions as SQL Assistant."})
        openai.api_key = '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'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context,
            max_tokens=max_tokens,
            temperature=temperature,
            #top_p=top_p,
            #frequency_penalty=frequency_penalty,
            #presence_penalty=presence_penalty,
            #stop=stop,
            
            )
        self.context.append({'role':'assistant', 'content':f"{response}"})
        return response