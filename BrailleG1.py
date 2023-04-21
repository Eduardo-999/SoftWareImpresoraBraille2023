from flet import *
import numpy as np
import time
class Translate_To_Braiile(UserControl):
    def __init__(self, page: Page, TextFieldToTranslate, Show_Coordinates):
        super().__init__()
        self.page = page
        self.TextFieldToTranslate = TextFieldToTranslate
        self.Show_Coordinates = Show_Coordinates
        self.N_Cajetines = 30
        self.N_Renglones = 20
        self.Superior = 1
        self.Inferior = 1
        self.Izquierda = 1
        self.Derecha = 1
        self.a = 2.55
        self.b = 2.55
        self.c = 6.39
        self.d = 10.54
        self.CodBraille = {
        # Alfabeto en minusculas:
            "a": ["⠁", [
                        
                            [1, 0], 
                            [0, 0], 
                            [0, 0]
                        
                        ], "Mi"],
            "b": ["⠃", [[1, 0], [1, 0], [0, 0]], "Mi"],
            "c": ["⠉", [[1, 1], [0, 0], [0, 0]], "Mi"],
            "d": ["⠙", [[1, 1], [0, 1], [0, 0]], "Mi"],
            "e": ["⠑", [[1, 0], [0, 1], [0, 0]], "Mi"],
            "f": ["⠋", [[1, 1], [1, 0], [0, 0]], "Mi"],
            "g": ["⠛", [[1, 1], [1, 1], [0, 0]], "Mi"],
            "h": ["⠓", [[1, 0], [1, 1], [0, 0]], "Mi"],
            "i": ["⠊", [[0, 1], [1, 0], [0, 0]], "Mi"],
            "j": ["⠚", [[0, 1], [1, 1], [0, 0]], "Mi"],
            "k": ["⠅", [[1, 0], [0, 0], [1, 0]], "Mi"],
            "l": ["⠇", [[1, 0], [1, 0], [1, 0]], "Mi"],
            "m": ["⠍", [[1, 1], [0, 0], [1, 0]], "Mi"],
            "n": ["⠝", [[1, 1], [0, 1], [1, 0]], "Mi"],
            "o": ["⠕", [[1, 0], [0, 1], [1, 0]], "Mi"],
            "p": ["⠏", [[1, 1], [1, 0], [1, 0]], "Mi"],
            "q": ["⠟", [[1, 1], [1, 1], [1, 0]], "Mi"],
            "r": ["⠗", [[1, 0], [1, 1], [1, 0]], "Mi"],
            "s": ["⠎", [[0, 1], [1, 0], [1, 0]], "Mi"],
            "t": ["⠞", [[0, 1], [1, 1], [1, 0]], "Mi"],
            "u": ["⠥", [[1, 0], [0, 0], [1, 1]], "Mi"],
            "v": ["⠧", [[1, 0], [1, 0], [1, 1]], "Mi"],
            "w": ["⠺", [[0, 1], [1, 1], [0, 1]], "Mi"],
            "x": ["⠭", [[1, 1], [0, 0], [1, 1]], "Mi"],
            "y": ["⠽", [[1, 1], [0, 1], [1, 1]], "Mi"],
            "z": ["⠵", [[1, 0], [0, 1], [1, 1]], "Mi"],
        # Alfabeto en mayusculas:
            "A": ["⠁", [[1, 0], [0, 0], [0, 0]], "Ma"],
            "B": ["⠃", [[1, 0], [1, 0], [0, 0]], "Ma"],
            "C": ["⠉", [[1, 1], [0, 0], [0, 0]], "Ma"],
            "D": ["⠙", [[1, 1], [0, 1], [0, 0]], "Ma"],
            "E": ["⠑", [[1, 0], [0, 1], [0, 0]], "Ma"],
            "F": ["⠋", [[1, 1], [1, 0], [0, 0]], "Ma"],
            "G": ["⠛", [[1, 1], [1, 1], [0, 0]], "Ma"],
            "H": ["⠓", [[1, 0], [1, 1], [0, 0]], "Ma"],
            "I": ["⠊", [[0, 1], [1, 0], [0, 0]], "Ma"],
            "J": ["⠚", [[0, 1], [1, 1], [0, 0]], "Ma"],
            "K": ["⠅", [[1, 0], [0, 0], [1, 0]], "Ma"],
            "L": ["⠇", [[1, 0], [1, 0], [1, 0]], "Ma"],
            "M": ["⠍", [[1, 1], [0, 0], [1, 0]], "Ma"],
            "N": ["⠝", [[1, 1], [0, 1], [1, 0]], "Ma"],
            "O": ["⠕", [[1, 0], [0, 1], [1, 0]], "Ma"],
            "P": ["⠏", [[1, 1], [1, 0], [1, 0]], "Ma"],
            "Q": ["⠟", [[1, 1], [1, 1], [1, 0]], "Ma"],
            "R": ["⠗", [[1, 0], [1, 1], [1, 0]], "Ma"],
            "S": ["⠎", [[0, 1], [1, 0], [1, 0]], "Ma"],
            "T": ["⠞", [[0, 1], [1, 1], [1, 0]], "Ma"],
            "U": ["⠥", [[1, 0], [0, 0], [1, 1]], "Ma"],
            "V": ["⠧", [[1, 0], [1, 0], [1, 1]], "Ma"],
            "W": ["⠺", [[0, 1], [1, 1], [0, 1]], "Ma"],
            "X": ["⠭", [[1, 1], [0, 0], [1, 1]], "Ma"],
            "Y": ["⠽", [[1, 1], [0, 1], [1, 1]], "Ma"],
            "Z": ["⠵", [[1, 0], [0, 1], [1, 1]], "Ma"],
        # diacriticos: "áéíóúüñ"
            "á": ["⠷", [[1, 0], [1, 1], [1, 1]], "Mi"],
            "é": ["⠮", [[0, 1], [1, 0], [1, 1]], "Mi"],
            "í": ["⠌", [[0, 1], [0, 0], [1, 0]], "Mi"],
            "ó": ["⠬", [[0, 1], [0, 0], [1, 1]], "Mi"],
            "ú": ["⠾", [[0, 1], [1, 1], [1, 1]], "Mi"],
            "ü": ["⠳", [[1, 0], [1, 1], [0, 1]], "Mi"],
            "ñ": ["⠻", [[1, 1], [1, 1], [0, 1]], "Mi"],

            "Á": ["⠷", [[1, 0], [1, 1], [1, 1]], "Ma"],
            "É": ["⠮", [[0, 1], [1, 0], [1, 1]], "Ma"],
            "Í": ["⠌", [[0, 1], [0, 0], [1, 0]], "Ma"],
            "Ó": ["⠬", [[0, 1], [0, 0], [1, 1]], "Ma"],
            "Ú": ["⠾", [[0, 1], [1, 1], [1, 1]], "Ma"],
            "Ü": ["⠳", [[1, 0], [1, 1], [0, 1]], "Ma"],
            "Ñ": ["⠻", [[1, 1], [1, 1], [0, 1]], "Ma"],
        # Numeros:
            "0": ["⠚", [[0, 1], [1, 1], [0, 0]], "N"],
            "1": ["⠁", [[1, 0], [0, 0], [0, 0]], "N"],
            "2": ["⠃", [[1, 0], [1, 0], [0, 0]], "N"],
            "3": ["⠉", [[1, 1], [0, 0], [0, 0]], "N"],
            "4": ["⠙", [[1, 1], [0, 1], [0, 0]], "N"],
            "5": ["⠑", [[1, 0], [0, 1], [0, 0]], "N"],
            "6": ["⠋", [[1, 1], [1, 0], [0, 0]], "N"],
            "7": ["⠛", [[1, 1], [1, 1], [0, 0]], "N"],
            "8": ["⠓", [[1, 0], [1, 1], [0, 0]], "N"],
            "9": ["⠊", [[0, 1], [1, 0], [0, 0]], "N"],
        # Signos de puntuacion:
            '.': ["⠄", [[0, 0], [0, 0], [1, 0]], "P"],
            ',': ["⠂", [[0, 0], [1, 0], [0, 0]], "P"],
            ';': ["⠆", [[0, 0], [1, 0], [1, 0]], "P"],
            ':': ["⠒", [[0, 0], [1, 1], [0, 0]], "P"],
            '-': ["⠤", [[0, 0], [0, 0], [1, 1]], "P"],
            '?': ["⠢", [[0, 0], [1, 0], [0, 1]], "P"],
            '¿': ["⠢", [[0, 0], [1, 0], [0, 1]], "P"],
            '!': ["⠖", [[0, 0], [1, 1], [1, 0]], "P"],
            '¡': ["⠖", [[0, 0], [1, 1], [1, 0]], "P"],
            '"': ["⠦", [[0, 0], [1, 0], [1, 1]], "P"],
            "“": ["⠦", [[0, 0], [1, 0], [1, 1]], "P"],
            "”": ["⠦", [[0, 0], [1, 0], [1, 1]], "P"],
            '(': ["⠣", [[1, 0], [1, 0], [0, 1]], "P"],
            ')': ["⠜", [[0, 1], [0, 1], [1, 0]], "P"],
            '*': ["⠔", [[0, 0], [0, 1], [1, 0]], "P"],
            '=': ["⠶", [[0, 0], [1, 1], [1, 1]], "P"],
            '+': ["⠖", [[0, 0], [1, 1], [1, 0]], "P"],
            '|': ["⠸", [[0, 1], [0, 1], [0, 1]], "P"],
            '\'': ["⠄", [[0, 0], [0, 0], [1, 0]], "P"],
            '[': ["⠷", [[1, 0], [1, 1], [1, 1]], "P"],
            ']': ["⠾", [[0, 1], [1, 1], [1, 1]], "P"],
            '@': ["⠐", [[0, 0], [0, 1], [0, 0]], "P"],
            '#': ["⠼⠐", [[[0, 1], [0, 1], [1, 1]], [[0, 0], [0, 1], [0, 0]]], "P"],
            '$': ["⠸⠜", [[[0, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [1, 0]]], "P"],
            '%': ["⠸⠴", [[[0, 1], [0, 1], [0, 1]], [[0, 0], [0, 1], [1, 1]]], "P"],
            '&': ["⠠⠯", [[[0, 0], [0, 0], [1, 0]], [[1, 1], [1, 0], [1, 1]]], "P"],
            '/': ["⠠⠂", [[[0, 0], [0, 0], [0, 1]], [[0, 0], [1, 0], [0, 0]]], "P"],
            '\\': ["⠐⠄", [[[0, 0], [0, 1], [0, 0]], [[0, 0], [0, 0], [1, 0]]], "P"],
            '{': ["⠐⠸", [[[0, 0], [0, 1], [0, 0]], [[0, 1], [0, 1], [0, 1]]], "P"],
            '}': ["⠸⠂", [[[0, 1], [0, 1], [0, 1]], [[0, 0], [1, 0], [0, 0]]], "P"],
            "'": ["⠠⠦", [[[0, 0], [0, 0], [0, 1]], [[0, 0], [1, 0], [1, 1]]], "P"],
            "‘": ["⠠⠦", [[[0, 0], [0, 0], [0, 1]], [[0, 0], [1, 0], [1, 1]]], "P"],
            "’": ["⠠⠦", [[[0, 0], [0, 0], [0, 1]], [[0, 0], [1, 0], [1, 1]]], "P"],
            ' ': [" ",   [[0, 0], [0, 0], [0, 0]], "esp"],
            '\n': ["\n", [[0, 0], [0, 0], [0, 0]], "sal"],
            '\t': ["\t", [[0, 0], [0, 0], [0, 0]], "tab"]
        }
        self.CodBraille2 = {
            # Alfabeto en minusculas:
            "⠁": [[1, 0], [0, 0], [0, 0]],
            "⠃": [[1, 0], [1, 0], [0, 0]],
            "⠉": [[1, 1], [0, 0], [0, 0]],
            "⠙": [[1, 1], [0, 1], [0, 0]],
            "⠑": [[1, 0], [0, 1], [0, 0]],
            "⠋": [[1, 1], [1, 0], [0, 0]],
            "⠛": [[1, 1], [1, 1], [0, 0]],
            "⠓": [[1, 0], [1, 1], [0, 0]],
            "⠊": [[0, 1], [1, 0], [0, 0]],
            "⠚": [[0, 1], [1, 1], [0, 0]],
            "⠅": [[1, 0], [0, 0], [1, 0]],
            "⠇": [[1, 0], [1, 0], [1, 0]],
            "⠍": [[1, 1], [0, 0], [1, 0]],
            "⠝": [[1, 1], [0, 1], [1, 0]],
            "⠕": [[1, 0], [0, 1], [1, 0]],
            "⠏": [[1, 1], [1, 0], [1, 0]],
            "⠟": [[1, 1], [1, 1], [1, 0]],
            "⠗": [[1, 0], [1, 1], [1, 0]],
            "⠎": [[0, 1], [1, 0], [1, 0]],
            "⠞": [[0, 1], [1, 1], [1, 0]],
            "⠥": [[1, 0], [0, 0], [1, 1]],
            "⠧": [[1, 0], [1, 0], [1, 1]],
            "⠺": [[0, 1], [1, 1], [0, 1]],
            "⠭": [[1, 1], [0, 0], [1, 1]],
            "⠽": [[1, 1], [0, 1], [1, 1]],
            "⠵": [[1, 0], [0, 1], [1, 1]],
            # Alfabeto en mayusculas:
            "⠁": [[1, 0], [0, 0], [0, 0]],
            "⠃": [[1, 0], [1, 0], [0, 0]],
            "⠉": [[1, 1], [0, 0], [0, 0]],
            "⠙": [[1, 1], [0, 1], [0, 0]],
            "⠑": [[1, 0], [0, 1], [0, 0]],
            "⠋": [[1, 1], [1, 0], [0, 0]],
            "⠛": [[1, 1], [1, 1], [0, 0]],
            "⠓": [[1, 0], [1, 1], [0, 0]],
            "⠊": [[0, 1], [1, 0], [0, 0]],
            "⠚": [[0, 1], [1, 1], [0, 0]],
            "⠅": [[1, 0], [0, 0], [1, 0]],
            "⠇": [[1, 0], [1, 0], [1, 0]],
            "⠍": [[1, 1], [0, 0], [1, 0]],
            "⠝": [[1, 1], [0, 1], [1, 0]],
            "⠕": [[1, 0], [0, 1], [1, 0]],
            "⠏": [[1, 1], [1, 0], [1, 0]],
            "⠟": [[1, 1], [1, 1], [1, 0]],
            "⠗": [[1, 0], [1, 1], [1, 0]],
            "⠎": [[0, 1], [1, 0], [1, 0]],
            "⠞": [[0, 1], [1, 1], [1, 0]],
            "⠥": [[1, 0], [0, 0], [1, 1]],
            "⠧": [[1, 0], [1, 0], [1, 1]],
            "⠺": [[0, 1], [1, 1], [0, 1]],
            "⠭": [[1, 1], [0, 0], [1, 1]],
            "⠽": [[1, 1], [0, 1], [1, 1]],
            "⠵": [[1, 0], [0, 1], [1, 1]],
            # diacriticos: "áéíóúüñ"
            "⠷": [[1, 0], [1, 1], [1, 1]],
            "⠮": [[0, 1], [1, 0], [1, 1]],
            "⠌": [[0, 1], [0, 0], [1, 0]],
            "⠬": [[0, 1], [0, 0], [1, 1]],
            "⠾": [[0, 1], [1, 1], [1, 1]],
            "⠳": [[1, 0], [1, 1], [0, 1]],
            "⠻": [[1, 1], [1, 1], [0, 1]],

            "⠷": [[1, 0], [1, 1], [1, 1]],
            "⠮": [[0, 1], [1, 0], [1, 1]],
            "⠌": [[0, 1], [0, 0], [1, 0]],
            "⠬": [[0, 1], [0, 0], [1, 1]],
            "⠾": [[0, 1], [1, 1], [1, 1]],
            "⠳": [[1, 0], [1, 1], [0, 1]],
            "⠻": [[1, 1], [1, 1], [0, 1]],
            # Numeros:
            "⠚": [[0, 1], [1, 1], [0, 0]],
            "⠁": [[1, 0], [0, 0], [0, 0]],
            "⠃": [[1, 0], [1, 0], [0, 0]],
            "⠉": [[1, 1], [0, 0], [0, 0]],
            "⠙": [[1, 1], [0, 1], [0, 0]],
            "⠑": [[1, 0], [0, 1], [0, 0]],
            "⠋": [[1, 1], [1, 0], [0, 0]],
            "⠛": [[1, 1], [1, 1], [0, 0]],
            "⠓": [[1, 0], [1, 1], [0, 0]],
            "⠊": [[0, 1], [1, 0], [0, 0]],
            # Signos de puntuacion:
            "⠄": [[0, 0], [0, 0], [1, 0]],
            "⠂": [[0, 0], [1, 0], [0, 0]],
            "⠆": [[0, 0], [1, 0], [1, 0]],
            "⠒": [[0, 0], [1, 1], [0, 0]],
            "⠤": [[0, 0], [0, 0], [1, 1]],
            "⠢": [[0, 0], [1, 0], [0, 1]],
            "⠖": [[0, 0], [1, 1], [1, 0]],
            "⠖": [[0, 0], [1, 1], [1, 0]],
            "⠦": [[0, 0], [1, 0], [1, 1]],
            "⠣": [[1, 0], [1, 0], [0, 1]],
            "⠜": [[0, 1], [0, 1], [1, 0]],
            "⠔": [[0, 0], [0, 1], [1, 0]],
            "⠶": [[0, 0], [1, 1], [1, 1]],
            "⠖": [[0, 0], [1, 1], [1, 0]],
            "⠸": [[0, 1], [0, 1], [0, 1]],
            "⠄": [[0, 0], [0, 0], [1, 0]],
            "⠷": [[1, 0], [1, 1], [1, 1]],
            "⠾": [[0, 1], [1, 1], [1, 1]],
            "⠐": [[0, 0], [0, 1], [0, 0]],
            "⠨": [[0, 1], [0, 0], [0, 1]],
            "⠐": [[0, 0], [0, 1], [0, 0]],
            "⠼": [[0, 1], [0, 1], [1, 1]],
            "⠠": [[0, 0], [0, 0], [0, 1]],
            "⠴": [[0, 0], [0, 1], [1, 1]],

            "⠼⠐": [[[0, 1], [0, 1], [1, 1]], [[0, 0], [0, 1], [0, 0]]],
            "⠸⠜": [[[0, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [1, 0]]],
            "⠸⠴": [[[0, 1], [0, 1], [0, 1]], [[0, 0], [0, 1], [1, 1]]],
            "⠠⠯": [[[0, 0], [0, 0], [1, 0]], [[1, 1], [1, 0], [1, 1]]],
            "⠠⠂": [[[0, 0], [0, 0], [0, 1]], [[0, 0], [1, 0], [0, 0]]],
            "⠐⠄": [[[0, 0], [0, 1], [0, 0]], [[0, 0], [0, 0], [1, 0]]],
            "⠐⠸": [[[0, 0], [0, 1], [0, 0]], [[0, 1], [0, 1], [0, 1]]],
            "⠸⠂": [[[0, 1], [0, 1], [0, 1]], [[0, 0], [1, 0], [0, 0]]]
        }
        
        
    def Word(self, Cadena): 
        Datos = []
        N_Letras = 0
        N_Espacios = 0
        N_Palabras = 0
        N_Saltos = 0
        IndiceCadena = 0
        for Item in Cadena:
            if str.isspace(Item): # Si es un espacio
                if Item == " ": # Si es un espacio simple
                    if N_Letras > 0:
                        Datos.append([N_Palabras, Cadena[IndiceCadena-N_Letras: IndiceCadena],len(Cadena[IndiceCadena-N_Letras: IndiceCadena])])
                        N_Palabras = N_Palabras + 1
                    N_Espacios = N_Espacios + 1
                    N_Letras = 0
                elif Item == "\n": # Si es un salto de linea
                    if N_Letras > 0:
                        Datos.append([N_Palabras, Cadena[IndiceCadena-N_Letras: IndiceCadena],len(Cadena[IndiceCadena-N_Letras: IndiceCadena])])
                        N_Palabras = N_Palabras + 1
                    N_Saltos = N_Saltos + 1
                    N_Letras = 0
                elif Item == "\t": # Si es un tabulador
                    if N_Letras > 0:
                        N_Palabras = N_Palabras + 1
                        Datos.append([N_Palabras, Cadena[IndiceCadena-N_Letras: IndiceCadena],len(Cadena[IndiceCadena-N_Letras: IndiceCadena])])
                    N_Espacios = N_Espacios + 8
                    N_Letras = 0
            else:
                N_Letras = N_Letras + 1
            IndiceCadena = IndiceCadena + 1
        if N_Letras > 0:
            Datos.append([N_Palabras, Cadena[IndiceCadena-N_Letras: IndiceCadena],len(Cadena[IndiceCadena-N_Letras: IndiceCadena])])
            N_Palabras = N_Palabras + 1
        return Datos

    def Conversion(self, Text_To_Braille): # Converts text to Braille grade 1
        """This function converts text to Braille grade 1"""
        TextCovert = ""
        NUMERAL = False
        MAYUSS = False
        contador = 0
        for item in Text_To_Braille:
            # Sí es un número
            if (self.CodBraille[item][2] == "N"):  # Si es un número
                if (not NUMERAL): # Viene de un caracter diferente a numero
                    NUMERAL = True
                    #print("⠼", end="")
                    TextCovert = TextCovert + "⠼"
                # Viene de un numero
                #print(CodBraille[item][0], end="")
                TextCovert = TextCovert + self.CodBraille[item][0]
                MAYUSS =False

            # Sí es minúscula o puntuación
            elif (self.CodBraille[item][2] == "Mi" or self.CodBraille[item][2] == "P"):
                if NUMERAL:
                    #print("⠐", end="")
                    TextCovert = TextCovert + "⠐"
                #print(CodBraille[item][0], end="")
                TextCovert = TextCovert + self.CodBraille[item][0]
                NUMERAL = False
                MAYUSS =False

            # Sí es mayúscula
            elif (self.CodBraille[item][2] == "Ma"):  
                if not MAYUSS:
                    MAYUSS = True
                    # Texto de ejemplo LALO

                    if contador+1 <= len(Text_To_Braille):
                        if (self.CodBraille[Text_To_Braille[contador+1]][2] == "Ma"):
                            #print(item + " :: " + texto[contador+1])    
                            #print("⠨⠨", end="")
                            TextCovert = TextCovert + "⠨⠨"
                        else: 
                            #print("⠨", end="")
                            TextCovert = TextCovert + "⠨"
                
                #print(CodBraille[item][0], end="")
                TextCovert = TextCovert + self.CodBraille[item][0]
                NUMERAL = False
            
            # Sí es salto de linea   
            elif self.CodBraille[item][2] == "sal":
                #print(item, end="")
                TextCovert = TextCovert + item
                NUMERAL = False
                MAYUSS =False
            
            # Sí es espacio
            elif self.CodBraille[item][2] == "esp":
                #print(item, end="")
                TextCovert = TextCovert + item
                NUMERAL = False
                MAYUSS =False

            # Sí es tabulador
            elif self.CodBraille[item][2] == "tab":
                #print(item, end="")
                TextCovert = TextCovert + item
                NUMERAL = False
                MAYUSS =False

            contador = contador + 1
        return TextCovert

    def TranslateGradeOne(self, TextBlock):
        TextBlockBraille = self.Conversion(TextBlock) # Block of text in braille (hello world => ⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙)
        SchemeBlockBraille = self.Word(TextBlockBraille) # Scheme of the block of text in braille => (Number of words, word in Braille, length of word in Braille)
        cajetin = 0
        renglon = 0
        cursor = 0
        FlagSpace = False
        for character in TextBlockBraille: # for each character in the block of text in braille
            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + character # add the character to the text field to translate
            if str.isspace(character):  # if character is space
                if character == ' ': # if character is space
                    if not FlagSpace: 
                        if (self.N_Cajetines - cajetin) > 0: # if there is space
                            cajetin = cajetin + 1 # add a box
                            FlagSpace = True # space flag
                        else: # if there is no space
                            renglon = renglon + 1 # next line
                            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                            cajetin = 0 # reset the box
                            if not (renglon >= self.N_Renglones): # if the line is greater than the number of lines
                                cajetin = cajetin + 1 # add a box
                                FlagSpace = True # space flag
                        cursor = cursor + 1 # next character
                    else:
                        if (self.N_Cajetines - cajetin) > 0: # if there is space
                            cajetin = cajetin + 1 # add a box
                        else:
                            renglon = renglon + 1 # next line
                            cajetin = 0 # reset the box
                            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                            cajetin = cajetin + len(" ") # add a box
                    if cursor >= len(SchemeBlockBraille): # if the cursor is greater than the length of the scheme
                        cursor = len(SchemeBlockBraille) # set the cursor to the length of the scheme
                    if SchemeBlockBraille[cursor][2] > self.N_Cajetines - cajetin: # if the word is longer than the box
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                elif character == '\n': # if letter is new line
                    if not FlagSpace: # if there is no space
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        FlagSpace = True # space flag
                        cursor = cursor + 1 # next character
                    else: # if there is space
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                        
                elif character == '\t': # if letter is tab
                    cursor = cursor + 1 # next character
                    if 8 <= (self.N_Cajetines - cajetin): # if there is space
                        cajetin = cajetin + 8 # add 8 boxes
                    else: # if there is no space
                        cajetin = 0 # reset the box
                        renglon = renglon + 1 # next line
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
            else: # if character is not space
                FlagSpace = False # reset the space flag
                cajetin = cajetin + len(character) # add a box
            if renglon >= self.N_Renglones: # if the line is greater than the number of lines
                cajetin = 0 # reset the box
                renglon = 0 # reset the line
    
    def GetCoordinates(self, TextBlockBraille, _Row): # Get the coordinates of the box
        ColumnBinary = ""
        PosX = 0
        Cursor_One = 0
        for Character_Braille in TextBlockBraille: # for each character in the block
            #print(Character_Braille, end="") # print the character in braille
            if Character_Braille == ' ':
                BrailleBin = self.CodBraille[Character_Braille][1] # get the matrix 2x3 of the character in braille
                BrailleBin = np.transpose(BrailleBin)
                BrailleBin = np.flip(BrailleBin, axis=1)
                Cursor_Two = 0
                PosX = (self.c * Cursor_One)
                for i in BrailleBin: # for each row in the matrix 
                    for j in i: # for each column in the matrix 
                        ColumnBinary += str(j)
                    self.Show_Coordinates.value = "X: " + str(round(PosX + (self.a * Cursor_Two), 2)) + " Y: " + str(round(_Row, 2)) + " Bin: " + str(int(ColumnBinary, 2))
                    print(self.Show_Coordinates.value)
                    self.page.update()
                    time.sleep(0.05)
                    ColumnBinary = ""
                    Cursor_Two += 1

            elif Character_Braille == '\t':
                pass
            elif Character_Braille == '\n':
                print()
            else:
                BrailleBin = self.CodBraille2[Character_Braille] # get the matrix 2x3 of the character in braille
                BrailleBin = np.transpose(BrailleBin)
                BrailleBin = np.flip(BrailleBin, axis=1)
                Cursor_Two = 0
                PosX = (self.c * Cursor_One)
                for i in BrailleBin: # for each row in the matrix 
                    for j in i: # for each column in the matrix 
                        ColumnBinary += str(j)
                    self.Show_Coordinates.value = "X: " + str(round(PosX + (self.a * Cursor_Two), 2)) + " Y: " + str(round(_Row, 2)) + " Bin: " + str(int(ColumnBinary, 2))
                    print(self.Show_Coordinates.value)
                    self.page.update()
                    time.sleep(0.05)
                    ColumnBinary = ""
                    Cursor_Two += 1
            Cursor_One += 1
        return _Row
               
    def FormatTextBraille(self, TextBraille): # Format the text in braille
        SchemeBlockBraille = self.Word(TextBraille) # Scheme of the block of text in braille => (Number of words, word in Braille, length of word in Braille)
        print(SchemeBlockBraille)
        cajetin = 0
        renglon = 0
        cursor = 0
        FlagSpace = False
        for character in TextBraille: # for each character in the block of text in braille
            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + character # add the character to the text field to translate
            if str.isspace(character):  # if character is space
                if character == ' ': # if character is space
                    if not FlagSpace: 
                        if (self.N_Cajetines - cajetin) > 0: # if there is space
                            cajetin = cajetin + 1 # add a box
                            FlagSpace = True # space flag
                        else: # if there is no space
                            renglon = renglon + 1 # next line
                            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                            cajetin = 0 # reset the box
                            if not (renglon >= self.N_Renglones): # if the line is greater than the number of lines
                                cajetin = cajetin + 1 # add a box
                                FlagSpace = True # space flag
                        cursor = cursor + 1 # next character
                    else:
                        if (self.N_Cajetines - cajetin) > 0: # if there is space
                            cajetin = cajetin + 1 # add a box
                        else:
                            renglon = renglon + 1 # next line
                            cajetin = 0 # reset the box
                            self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                            cajetin = cajetin + len(" ") # add a box
                    if cursor >= len(SchemeBlockBraille): # if the cursor is greater than the length of the scheme
                        cursor = len(SchemeBlockBraille) # set the cursor to the length of the scheme
                    if SchemeBlockBraille[cursor][2] > self.N_Cajetines - cajetin: # if the word is longer than the box
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                elif character == '\n': # if letter is new line
                    if not FlagSpace: # if there is no space
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        FlagSpace = True # space flag
                        cursor = cursor + 1 # next character
                    else: # if there is space
                        renglon = renglon + 1 # next line
                        cajetin = 0 # reset the box
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
                        
                elif character == '\t': # if letter is tab
                    cursor = cursor + 1 # next character
                    if 8 <= (self.N_Cajetines - cajetin): # if there is space
                        cajetin = cajetin + 8 # add 8 boxes
                    else: # if there is no space
                        cajetin = 0 # reset the box
                        renglon = renglon + 1 # next line
                        self.TextFieldToTranslate.value = self.TextFieldToTranslate.value + '\n' # new line
            else: # if character is not space
                FlagSpace = False # reset the space flag
                cajetin = cajetin + len(character) # add a box
            if renglon >= self.N_Renglones: # if the line is greater than the number of lines
                cajetin = 0 # reset the box
                renglon = 0 # reset the line
                
   