
# Cultura Viva - 🌄 Predicción de Culturas Ecuatorianas con IA + Geolocalización + Chatbot


Este proyecto implementa una plataforma web interactiva que permite predecir a qué cultura ecuatoriana pertenece una imagen usando un modelo de Deep Learning entrenado, mostrar su ubicación en Google Maps y acceder a información cultural a través de un chatbot entrenado con GPT2 y frases con información relevante de cada cultura.

---

## Estructura del Proyecto

```
login-app/
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   └── static/
│       └── styles.css
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Funcionalidades Principales

- 🔐 **Sistema de Login Seguro** con Flask y MySQL
- 🧠 **Predicción de culturas** mediante imágenes usando un modelo entrenado (MobileNetV2)
- 🗺️ **Ubicación automática en Google Maps** de la cultura detectada
- 🤖 **Chatbot informativo** que responde sobre la cultura identificada
- 🎨 Interfaz visual atractiva y sencilla

---

## 🧠 Culturas Soportadas

- Achuar  
- Afroecuatoriano *(redirige automáticamente al Valle del Chota)*  
- Cañari  
- Cayambis  
- Kichwa  
- Puruhua  
- Salasacas  
- Saraguro  
- Shuar  

---

## Tecnologías Utilizadas

- Python 3.12  
- Flask  
- MySQL  
- Docker & Docker Compose  
- bcrypt (hashing de contraseñas)  
- Google Maps (por URL pública)  
- Chatbot modelo GPT2 

## Configuración

1. **Clonar el repositorio:**

```bash
git clone https://github.com/BrieLy07/CulturaViva.git
cd CulturaViva
```

2. **Editar variables de entorno si es necesario:**

Dentro de `app.py` puedes modificar los valores por defecto de la conexión a la base de datos.

3. **Construir y levantar el proyecto:**

```bash
docker-compose up --build
```

4. **Acceder a la aplicación:**

Abre tu navegador en `http://localhost:5000`

---

## 🗺️ Ubicación en Google Maps

- Tras la predicción, se muestra un botón "Ver Ubicación" que:

- Redirige automáticamente a Google Maps con la cultura encontrada.

- Si la cultura es afroecuatoriano, muestra directamente el Valle del Chota.

- Si es Desconocido, el botón se desactiva para evitar errores.

---

## 🧠 Chatbot Cultural

- En desarrollo: el sistema integrará un chatbot entrenado con información de cada cultura, para responder preguntas como:

- ¿Dónde viven los Saraguro?

- ¿Qué vestimenta usan los Cañari?

- ¿Cuál es el idioma de los Shuar?

## Autor

Desarrollado por Briely07 y AndyDev
