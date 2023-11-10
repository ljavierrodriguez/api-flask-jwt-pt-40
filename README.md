# Proyecto con FLASK y PostgreSQL

1. Crear carpeta y abrirla con vscode

2. Crear archivo Pipfile

3. Crear y activar entorno virtual para trabajar, desde el terminal ejecutar

```shell
pipenv shell
```
4. Instalar los siguientes modulos:

```shell
pipenv install flask flask-migrate flask-sqlalchemy flask-cors python-dotenv psycopg2-binary
```

5. Crear el archivo ***.env*** en la carpeta principal y agregar el siguiente contenido:

```env
DATABASEURI="postgresql+psycopg2://postgres:postgres@localhost:5432/<database>"
```

6. Crear la carpeta ***src/*** y dentro crear dos archivos uno llamado ***app.py*** y un archivo llamado ***models.py***

7. En el archivo ***models.py*** agregar las siguientes lineas de codigo:

```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

8. En el archivo ***app.py*** agregar las siguientes importaciones

```python
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
```

9. Cargar las variables de entorno del archivo ***.env***

```python
load_dotenv() # cargar las variables de entorno
```

10. Instanciar una variable de Flask

```python
app = Flask(__name__)
```

11. Configurar parametros de opciones de flask

```python

app.config['DEBUG'] = True # Permite ver los errores
app.config['ENV'] = 'development' # Activa el servidor en modo desarrollo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI') # Leemos la url de conexion a la base de datos

```

12. Vincular el archivo ***models.py*** a nuestro archivo ***app.py***

```python
db.init_app(app)
```

13. Habilitar los comandos para crear las migraciones

```python
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
```

14. Crear modelo de ejemplo en el archivo ***models.py***:

```python 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

```

15. Habilitar el comando flask en el terminal (flask):

windows
```shell
SET FLASK_APP=src/app.py
```

Linux o Mac
```shell
export FLASK_APP=src/app.py
```

16. Ejecutar los comandos de las migraciones

Crear la carpeta migrations esto es solo la primera vez 
```shell
flask db init
```

Crear las migraciones
```shell
flask db migrate
```

Generar las migraciones en la base de datos
```shell
flask db upgrade
```

17. Crear endpoint principal

```python
@app.route('/')
def main():
    return jsonify({ "status": "Server Up"}), 200
```

18. Validamos nuestra aplicacion

```python
if __name__ == '__main__':
    app.run()
```

19. Iniciar nuestra app desde el terminal ("python3" si estoy en maco o linux, "python" si estoy en windows) 

```shell
python src/app.py
```
