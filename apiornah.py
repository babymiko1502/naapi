from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

html_template = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Limpiar N/A</title>
</head>
<body style="font-family:sans-serif;max-width:700px;margin:30px auto;">
  <h2>Eliminar N/A y extraer solo números</h2>
  <form method="POST" action="/procesar">
    <label>Pega tu lista (formato: N/A[TAB]número):</label><br><br>
    <textarea name="entrada" rows="15" cols="70" placeholder="N/A\t3104042303\nN/A\t3104042304">{{ entrada }}</textarea><br><br>
    <button type="submit">Limpiar</button>
  </form>

  {% if resultado %}
    <h3>Resultado (solo números):</h3>
    <textarea rows="15" cols="70">{{ resultado }}</textarea><br><br>
    <form method="POST" action="/descargar">
      <input type="hidden" name="contenido" value="{{ resultado | replace('\n', '&#10;') }}">
      <button type="submit">Descargar TXT</button>
    </form>
  {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template, entrada='', resultado=None)

@app.route('/procesar', methods=['POST'])
def procesar():
    texto = request.form.get('entrada', '')
    resultado = []

    for linea in texto.strip().splitlines():
        partes = linea.strip().split()
        if len(partes) == 2:
            resultado.append(partes[1])  # Solo el número

    return render_template_string(html_template,
                                  entrada=texto,
                                  resultado='\n'.join(resultado))

@app.route('/descargar', methods=['POST'])
def descargar():
    contenido = request.form.get('contenido', '')
    return Response(
        contenido,
        mimetype='text/plain',
        headers={'Content-Disposition': 'attachment;filename=numeros_limpios.txt'}
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
