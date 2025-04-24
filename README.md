
# Proyecto de Login Seguro con Docker Compose

Este proyecto implementa un sistema de login seguro usando Flask, MySQL y Docker Compose. Incorpora buenas prácticas como hashing de contraseñas, manejo de sesiones y un diseño visual atractivo.

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

## Tecnologías Utilizadas

- **Python 3.12**
- **Flask**
- **MySQL**
- **Docker & Docker Compose**
- **bcrypt**

## Configuración

1. **Clonar el repositorio:**

```bash
git clone https://github.com/BrieLy07/LoginFuncional.git
cd LoginFuncional
```

2. **Editar variables de entorno si es necesario:**

Dentro de `app.py` puedes modificar los valores por defecto de la conexión a la base de datos.

3. **Construir y levantar el proyecto:**

```bash
docker-compose up --build
```

4. **Acceder a la aplicación:**

Abre tu navegador en `http://localhost:5000`

## Funcionalidades

- Registro de usuarios con contraseñas hasheadas.
- Inicio de sesión seguro.
- Manejo de sesiones con Flask.
- Interfaz visual mejorada con HTML y CSS.
- Ruta protegida `/dashboard`.
- Cierre de sesión mediante `/logout`.

## Comandos útiles

**Subir imagen a Docker Hub:**

```bash
docker tag nombre_local brielys/loginimage:tagname
docker push brielys/loginimage:tagname
```

## Autor

Desarrollado por Briely07
