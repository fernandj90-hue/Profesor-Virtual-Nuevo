import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Configuración de OpenRouter
# NOTA: En Render, configuraremos la API_KEY como variable de entorno por seguridad
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free" 

@app.route("/", methods=["GET", "POST"])
def home():
    respuesta = None
    pregunta = None
    
    if request.method == "POST":
        pregunta = request.form.get("pregunta")
        
        # Llamada a la API de OpenRouter
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                },
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "Eres un Profesor Virtual experto. Explica temas de primaria y secundaria de forma sencilla, usando ejemplos claros y un lenguaje motivador."},
                        {"role": "user", "content": pregunta}
                    ]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                respuesta = data['choices'][0]['message']['content']
            else:
                respuesta = "Lo siento, mi cerebro electrónico tiene un problema técnico temporal."
        except Exception as e:
            respuesta = f"Error de conexión: {str(e)}"

    return render_template("index.html", pregunta=pregunta, respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)
