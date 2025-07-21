import secrets
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import bcrypt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

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

        return render_template('dashboard.html', cultura=cultura, confianza=round(confianza, 2))

    except Exception as e:
        return render_template('dashboard.html', cultura="Error: " + str(e), confianza=None)
    
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
