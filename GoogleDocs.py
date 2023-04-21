from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint

CredentialsGdocs = service_account.Credentials.from_service_account_file(
    'Key.json')# , scopes=SCOPES)
ServiceDocs = build('docs', 'v1', credentials=CredentialsGdocs)

def get_text(ID):
    datos = ServiceDocs.documents().get(documentId=ID).execute()
    TextToSend = ""
    for key in datos.keys():
        if type(datos[key]) == dict:
            for key2 in datos[key].keys():
                if type(datos[key][key2]) == dict:
                    pass
                elif type(datos[key][key2]) == list:
                    count = 0
                    for key3 in datos[key][key2]:
                        for key4 in key3.keys():
                            if key4 == "paragraph":
                                for element in datos[key][key2][count][key4].keys():
                                    if element == "elements":
                                        if type(datos[key][key2][count][key4][element]) == list:
                                            count2=0
                                            for element2 in datos[key][key2][count][key4][element]:
                                                for element3 in element2.keys():
                                                    if element3 == "textRun":
                                                        for claves in datos[key][key2][count][key4][element][count2].keys():
                                                            if claves == "textRun":
                                                                if (type(datos[key][key2][count][key4][element][count2][claves])) == dict:
                                                                    for clave2 in datos[key][key2][count][key4][element][count2][claves].keys():
                                                                        if clave2 == "content":
                                                                            #print(datos[key][key2][count][key4][element][count2][claves][clave2])
                                                                            TextToSend += datos[key][key2][count][key4][element][count2][claves][clave2]
                                                                        else:
                                                                            pass
                                                            elif claves == "inlineObjectElement":
                                                                if (type(datos[key][key2][count][key4][element][count2][claves])) == dict:
                                                                    for clave2 in datos[key][key2][count][key4][element][count2][claves].keys():
                                                                        if clave2 == "inlineObjectId":
                                                                            #print(datos[key][key2][count][key4][element][count2][claves][clave2])
                                                                            TextToSend += datos[key][key2][count][key4][element][count2][claves][clave2]
                                                                        else:
                                                                            pass
                                                        count2 += 1
                        count += 1
                else:
                    pass
        else:
            pass
    return TextToSend

#pprint.pprint(Sheet)

print(get_text('15qHwRU4n_LwdzLwp0xqcvveQtwQ1UijvVgxRSOIJtJw'))