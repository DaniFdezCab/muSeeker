
# MuSeeker

MuSeeker es una aplicación web desarrollada con Django, creada como parte de una asignatura. El objetivo principal de esta aplicación es permitir la búsqueda y obtención de información sobre álbumes de música. Los usuarios podrán explorar álbumes, obtener detalles y realizar búsquedas avanzadas basadas en varios criterios como el título, el artista, el género y más.

## Funcionalidades

- **Búsqueda de Álbumes**: Permite a los usuarios buscar álbumes de música por título, artista, género y otros criterios.
- **Detalles de Álbumes**: Muestra información detallada sobre los álbumes, incluyendo el nombre, la fecha de lanzamiento, las canciones y más.
- **Exploración de Artistas**: Los usuarios pueden explorar la discografía de los artistas y obtener información sobre su biografía y álbumes.
- **Interfaz de Usuario**: Una interfaz intuitiva y fácil de usar para realizar búsquedas y visualizar los resultados de manera clara.

## Instalación

Para comenzar a usar **MuSeeker**, sigue estos pasos:

### 1. Clonar el repositorio

```bash
git clone <url_del_repositorio>
cd MuSeeker
```

### 2. Crear y activar un entorno virtual

Crea un entorno virtual y actívalo en el directorio raíz del proyecto:

```bash
python -m venv venv
```

- En Windows:
  ```bash
  .env\Scriptsctivate
  ```
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar las dependencias

Con el entorno virtual activado, instala las dependencias necesarias con `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Ejecuta las migraciones para configurar la base de datos:

```bash
python manage.py migrate
```

### 5. Crear un superusuario (opcional)

Si deseas acceder al panel de administración de Django, crea un superusuario:

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Accede a la aplicación en `http://127.0.0.1:8000/`.

## Tecnologías Usadas

- **Django**: Framework web en Python para desarrollar la aplicación.
- **SQLite** (predeterminado): Base de datos ligera para el desarrollo y pruebas.
- **HTML, CSS, JavaScript**: Para la creación de la interfaz de usuario.
- **Bootstrap**: Framework CSS para hacer la interfaz más moderna y responsive.

## Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama nueva (`git checkout -b feature/mi-nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Empuja tus cambios a tu fork (`git push origin feature/mi-nueva-funcionalidad`).
5. Crea un pull request para que podamos revisar y fusionar tus cambios.
