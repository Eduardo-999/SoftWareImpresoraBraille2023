import os

# Ruta predeterminada del archivo de tema actual en Windows
theme_file_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Themes', 'CurrentTheme')

# Abrimos el archivo de tema y buscamos los valores de los colores del tema
with open(theme_file_path, 'r') as f:
    theme_data = f.read()
    color_values = [line.split('=')[1].strip() for line in theme_data.split('\n') if 'Color' in line]

# Imprimimos los valores de los colores del tema
print(color_values)

