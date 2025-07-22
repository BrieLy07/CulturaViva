import secrets
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import os
import requests
import bcrypt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from dotenv import load_dotenv
load_dotenv()

import os
HF_API_KEY = os.getenv("HF_API_KEY")

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt_sistema.txt")

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPT_INICIAL = f.read()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'

clases = ['achuar', 'afroecuatoriano', 'cañari', 'cayambis', 'kickwa', 'puruhua', 'salasacas', 'saraguro', 'shuar']
modelo = load_model("model/modelo_cultural_mobilenetv2.h5")

def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="login_db"
    )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales inválidas"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', cultura=None, confianza=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Las contraseñas no coinciden"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, phone, username, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, email, phone, username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'imagen' not in request.files:
        return render_template('dashboard.html', cultura="No se envió imagen", confianza=None)

    imagen = request.files['imagen']
    try:
        img = Image.open(imagen).convert("RGB")
        img = img.resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Guardar imagen para previsualización
        imagen_path = os.path.join("static", "ultima_imagen.png")
        img.save(imagen_path)

        pred = modelo.predict(img_array)
        indice = np.argmax(pred[0])
        confianza = float(pred[0][indice]) * 100

        if confianza < 49.0:
            cultura = "Desconocido"
        else:
            cultura = clases[indice]

        # 🔄 Normalización de nombres predichos
        normalizador = {
            'saraguro': 'saraguro',
            'otavalos': 'otavalo',
            'otavalo': 'otavalo',
            'salasacas': 'salasaca',
            'salasaca': 'salasaca',
            'cayambis': 'cayambis',
            'kichwa': 'kichwa amazónicos',
            'kichwas': 'kichwa amazónicos',
            'kichwa amazonico': 'kichwa amazónicos',
            'kichwa amazónicos': 'kichwa amazónicos',
            'shuar': 'shuar',
            'achuar': 'achuar',
            'chuar': 'achuar',
            'afroecuatoriano': 'afroecuatoriano',
            'afroecuatorianos': 'afroecuatoriano',
            'cañari': 'cañari',
            'canari': 'cañari',
            'cañaris': 'cañari',
            'puruhá': 'puruhá',
            'puruhas': 'puruhá',
            'puruhuaes': 'puruhá'
        }

        cultura_limpia = cultura.strip().lower()
        cultura = normalizador.get(cultura_limpia, cultura_limpia)

        return render_template('dashboard.html', cultura=cultura, confianza=round(confianza, 2))

    except Exception as e:
        return render_template('dashboard.html', cultura="Error: " + str(e), confianza=None)


 #Desde aqui todo lo relacionado con el chatbot
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/responder', methods=['POST'])
def responder():
    data = request.get_json()
    pregunta = data.get('mensaje', '')

    #Combinar el prompt profesional + la pregunta del usuario
    prompt_completo = PROMPT_INICIAL.strip() + f"\n\nUsuario: {pregunta}\nChatbot:"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": prompt_completo,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5,
            "top_p": 0.85,
            "repetition_penalty": 1.3
        }
    }

    modelo_url = "https://api-inference.huggingface.co/models/ItsAndy0/llama3-cultural-chatbot1-v2-merged"

    try:
        response = requests.post(modelo_url, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and 'generated_text' in result[0]:
            texto_generado = result[0]['generated_text']
            respuesta = texto_generado.split('Chatbot:')[-1].strip()
        else:
            respuesta = "⚠️ No se pudo obtener una respuesta válida del modelo."
    except Exception as e:
        respuesta = f"❌ Error al contactar el modelo: {str(e)}"

    return jsonify({"respuesta": respuesta})



if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)