import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Credentials manage to access to Google Drive
CredentialsGdrive = service_account.Credentials.from_service_account_file(
    'KeyGoogleDrive.json')
# Credentials manage to access to Google Docs
CredentialsGdocs = service_account.Credentials.from_service_account_file(
    'Key.json')# , scopes=SCOPES)

# Create an object to manage Google Drive
ServiceDrive = build('drive', 'v3', credentials=CredentialsGdrive)
# Create an object to manage Google Docs
ServiceDocs = build('docs', 'v1', credentials=CredentialsGdocs)

def descargar_archivo(archivo_id, nombre_archivo):
    try:
        # Descarga el archivo
        archivo = ServiceDrive.files().get_media(fileId=archivo_id).execute()

        # Escribe el contenido del archivo en un archivo local
        with io.FileIO(nombre_archivo, 'wb') as archivo_local:
            archivo_local.write(archivo)

        print(f'{nombre_archivo} se ha descargado correctamente.')

    except HttpError as error:
        print(f'Error al descargar el archivo: {error}')
def Get_ListFiles():
    List = []
    try:
        # Obtiene la lista de archivos en la cuenta de Drive
        resultados = ServiceDrive.files().list(
            fields='nextPageToken, files(id, name, mimeType, size, createdTime)').execute()
        
        # Muestra los nombres, tipos MIME, tamaños y fechas de creación de todos los archivos
        for archivo in resultados.get('files', []):
            #print(f"{archivo.get('name')} ({archivo.get('id')}) - {archivo.get('mimeType')} - {archivo.get('size')} bytes - Creado el {archivo.get('createdTime')}")
            List.append(
                [
                    archivo.get('id'), 
                    archivo.get('name'),
                    archivo.get('mimeType'), 
                    archivo.get('size'), 
                    archivo.get('createdTime')
                ]
            )
    except HttpError as error:
        print(f'Error al listar los archivos: {error}')
    return List
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

#if __name__ == '__main__':
    #descargar_archivo('1no12POGxl0ohvXHg0mdjFrKLlzUGgO8v', 'docu.docx')
#print(listar_archivos())
    #print(get_text('15qHwRU4n_LwdzLwp0xqcvveQtwQ1UijvVgxRSOIJtJw'))