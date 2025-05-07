# 🛠️ Backend Django - Proyecto RESTO ##

 ✅ Requisitos previos (no técnicos) 
 
 Antes de levantar el servidor, asegurate de tener: 
 - Acceso al archivo `.env` con las variables necesarias del entorno. 
 - Base de datos configurada y accesible (según tu `.env`). 
 - Conexión a internet si vas a instalar dependencias por primera vez. 
 --
 
  ## 🐍 Crear y activar el entorno virtual Si todavía no tenés un entorno virtual en el proyecto, podés crearlo con:
 
  ```python3 -m venv venv_ship ``` 
 
 
Una vez activado, deberías ver el prefijo `(venv_ship)` en tu terminal.
 ---
  ## 📦 Instalar dependencias 
 Con el entorno virtual activado, instalá todas las dependencias del proyecto con: 
 
 ```pip install -r requirements.txt ``` 
 
 Este comando lee el archivo `requirements.txt` y descarga automáticamente todos los paquetes necesarios para correr el proyecto. 
 
 --- 

 ## 🔍 Verificar existencia de base de datos
Para confirmar que la base de datos ya está creada, seguí estos pasos:

Ejecutá en la terminal:


``` psql -U postgres -l ```


Esto mostrará una lista de bases de datos. Buscá en la lista el nombre que definiste en PGDATABASE (por ejemplo, resto).

Si la base de datos no existe, creala:

Iniciá sesión en PostgreSQL:


``` psql -U postgres ``` 

password: postgres

En el prompt de PostgreSQL, ejecutá:


```CREATE DATABASE VER VARIABLE DE ENTORNO;```

Para salir:

``` \q ```
 
 ## ⚙️ Aplicar migraciones 
 
 Antes de levantar el servidor, asegurate de que todas las migraciones estén creadas y aplicadas:
 
  ```python manage.py makemigrations ```

   ```python manage.py migrate``` 
  
  Esto garantiza que las tablas en la base de datos estén actualizadas con los modelos definidos en el código.
  
 ---
 
## 🔐 Variables de entorno



El archivo `.env` debe existir en la raíz del proyecto y aprovechá el ejemplo y copialo:

``` cp .env.example .env ```



---


## 🧠 Enfoque de trabajo recomendado

Como este es tu primer proyecto en solitario, te recomendamos llevar un registro organizado de cada paso importante. Para eso:

- Creá una hoja en Notion (o tu herramienta favorita) **por cada componente nuevo que configures**.
- Ejemplos:
  - Si estás creando modelos en `models.py`, documentá qué representa cada uno y cómo se relacionan.
  - Si conectás la base de datos a un endpoint, explicá qué archivos tocaste (`views.py`, `urls.py`, etc.) y qué hace cada uno.

👉 Esto te va a ayudar a **entender mejor el flujo del proyecto** y a poder retomarlo fácilmente en el futuro o escalarlo.



👉👉👉👉👉👉👉 Esto fue mitad chatGPT y mitad DeepSeek amigo, claramente no lo escribí yo, **pero esto último es LO MAS IMPORTANTE,HACELO BIEN** 👉👉👉👉👉👉👉
