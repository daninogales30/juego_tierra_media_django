# Juego Tierra Media con Django

## Descripción del proyecto
Este proyecto es una implementación del Juego Tierra Media utilizando 
Django, un framework de Python de alto nivel especializado en el 
desarrollo web, API REST y dockerizandola con Docker. El permite gestionar diferentes aspectos 
del juego mediante una interfaz web.

El juego tiene 3 aplicaciones: `Battle`, `Character` y `Equipment`.

Cada aplicación tiene distintas funcionalidades relacionadas al nombre de la aplicación:
* La aplicación `Battle`
* La aplicación `Character` te permite crear personajes, gestionarlos y ver los detalles de cada uno. Puedes 
ver el listado de personajes, filtrarlos para ver cuales son de la raza humana, cuales tienen armas, etc.
* La aplicación `Equipment`

El juego te permite crear personajes, gestionarlos y ver los detalles de cada uno, añadir armas al inventario de estos personajes, equiparles las armas, 
iniciar relaciones entre ellos y hacerlos combatir en batallas.

## Estructura del Proyecto
Para comprender bien el funcionamiento del proyecto, una de las cosas que hay que 
saber como es la estructura del proyecto. 
A continuación, veremos el árbol de archivos y directorios de este proyecto.
```
├── templates/        # Plantillas del login y registro
├── juego_tierra_media_django/  # Carpeta principal
│   ├── settings.py   # Configuración del proyecto
│   └── urls.py       # Rutas del proyecto
├── requirements.txt  
├── manage.py         
├── docker-compose.yml
├── Dockerfile
├── README.md         # Documentación del proyecto (este archivo)
├── battle/           # App de batallas
│   ├── models.py     # Modelo para batalla
│   ├── views.py      # Vistas de la aplicacióm
│   ├── forms.py      # Formularios para gestionar batallas
│   ├── urls.py       # Rutas de la aplicación
│   ├── tests.py      # Pruebas unitarias
│   ├── templates/    # Plantilla HTML de batalla
│   ├── static/       # Archivos CSS e imágenes
│   └── migrations/   # Carpeta con las migraciones
│ 
├── character/        # App de personajes
│   ├── models.py     # Modelos de personajes y sus atributos
│   ├── serializers.py # Serializadores para API REST
│   ├── views.py      # Vistas de la aplicación
│   ├── forms.py      # Formularios para personajes
│   ├── urls.py       # Definición de rutas
│   ├── tests.py      # Pruebas unitarias
│   ├── templates/    # Plantillas HTML de personajes
│   ├── static/       # Archivos CSS, imágenes y archivo js para buscar personajes
│   └── migrations/   # Carpeta con las migraciones
│
└── equipment/        # App de equipamiento
    ├── models.py     # Modelos para objetos y equipamiento
    ├── signals.py    # Archivo que almacena armas precargadas
    ├── views.py      # Vistas del equipamiento
    ├── forms.py      # Formularios relacionados
    ├── urls.py       # Rutas de la aplicación
    ├── tests.py      # Pruebas unitarias
    ├── templates/    # Plantillas HTML del equipamiento
    ├── static/       # Archivos CSS e imágenes
    └── migrations/   # Carpeta con las migraciones

```

### Aplicacion `battle/`
#### **Modelos**
##### **Modelo `Battle`**

###### **Atributos Principales**
- `character1`: Primer personaje participante en la batalla.  
- `character2`: Segundo personaje participante en la batalla.  
- `winner`: Personaje que gana la batalla (puede estar vacío hasta que la batalla se simule).  
- `date`: Fecha y hora en la que se registró la batalla.  

###### **Métodos Principales**

- `simulate()`
Este método ejecuta la batalla entre los personajes y determina al ganador en función de la potencia de sus armas.  
  - **Verificaciones previas**: Ambos personajes deben tener un arma equipada.  
  - **Cálculo del ganador**:  
    - Se obtiene la potencia de cada arma.  
    - Se calcula la probabilidad de ganar según la fórmula:
    ```
      potencia_arma1 = self.character1.get_power()
      potencia_arma2 = self.character2.get_power()
      probabilidad1 = potencia_arma1 / (potencia_arma2 + potencia_arma1)
      resultado = random.random()
    ```
    - Se genera un número aleatorio para determinar el ganador.  
    - Se guarda el resultado en la base de datos. 

#### **Vistas**
`BattleView`: permite a los jugadores enfrentar a dos personajes en combate, verificando que ambos cumplan con los requisitos necesarios para pelear:
- **Formulario de batalla**: Utiliza `BattleForm` para seleccionar los personajes que participarán en la batalla.
- **Restricciones**:
  - Un personaje **no puede pelear contra sí mismo**.
  - Ambos personajes **deben tener un arma equipada** antes de la batalla.
- **Simulación de batalla**: Se crea una instancia de `Battle`, que simula el enfrentamiento y determina al ganador.



### Aplicacion `character/`
#### **Modelos**
##### **Modelo `Character`**
Representa a los personajes del juego con atributos como nombre, raza, facción, ubicación y equipamiento.
###### **Atributos Principales**
- `name`: Nombre único del personaje.
- `race`: Raza del personaje (Elfo, Humano, Enano, Hobbit).
- `faction`: Facción a la que pertenece el personaje.
- `ubication`: Ubicación actual del personaje en el mundo del juego.
- `equipment`: Equipamiento del personaje.
- `arma_equipada`: Arma actualmente equipada por el personaje.

###### **Métodos**
- `add_equipment(new_equipment)`: Añade un objeto al inventario del personaje.
- `equip_weapon(weapon)`: Equipa un arma al personaje si es válida.
- `change_ubication(new_ubication)`: Cambia la ubicación del personaje.
- `get_power()`: Devuelve la potencia del arma equipada.

##### **Modelo `Relacion`**
Permite definir los vínculos entre los personajes del juego, estableciendo el tipo de relación y un nivel de confianza entre ellos.
###### **Atributos Principales**
- `character`: El personaje que establece la relación.  
- `related_to`: El personaje con el que se relaciona.  
- `tipo`: Tipo de relación (`Amigo`, `Enemigo`, `Neutral`).  
- `confidence_level`: Nivel de confianza o cercanía en la relación.  

#### **Vistas**
- `RegistroUsuarioView`: Vista para el registro de usuarios.
- `StartGameView`: Vista protegida para la pantalla de inicio del juego.
- `PrincipalMenuView`: Vista protegida para el menú principal.
- `CreateCharacterView`: Vista para la creación de personajes.
- `DeleteCharacterView`: Vista para eliminar un personaje.
- `DetailCharacterView`: Vista para ver el detalle de un personaje.
- `EquipWeaponView`: Vista para equipar un arma a un personaje.
- `ChangeUbicationView`: Vista para cambiar la ubicación de un personaje.
- `RelacionCreateView`: Vista para la creación de relaciones entre personajes.
- `CharacterListView`: Vista para listar todos los personajes.
- `HumanosView`: Vista para listar personajes de la raza humana (consulta).
- `HumanosSinArmaView`: Vista para listar personajes humanos sin arma equipada (consulta).

#### **Vistas API REST**
- `RelacionViewSet`: Endpoints para gestionar relaciones entre personajes.
- `CharacterViewSet`: Endpoints para gestionar personajes con filtrado por nombre y facción.

#### **Formularios**
La aplicación utiliza formularios de Django para la creación y actualización relacionados con personajes y relaciones.

##### `CharacterForm`
Formulario basado en `ModelForm` para la gestión de personajes en la base de datos.

- **Modelo**: `Character`
- **Campos**: `name`, `race`, `faction`, `ubication`, `equipment`

###### Método principal
- `clean_name()`: Valida que no exista otro personaje con el mismo nombre.

##### `RelacionForm`
Formulario basado en `ModelForm` para la gestión de relaciones entre personajes.

- **Modelo**: `Relacion`
- **Campos**: `character`, `related_to`, `tipo`, `confidence_level`

###### Métodos principales
- `clean()`: Verifica que un personaje no pueda relacionarse consigo mismo.
- `save()`: Crea o actualiza una relación entre personajes utilizando `update_or_create()`.



### Aplicacion `equipment/`
#### **Modelos**
##### **Modelo `Equipment`**
El modelo `Equipment` representa un equipo dentro del sistema. Sus atributos son:
###### **Atributos Principales**
- `name`: Nombre único del equipo (cadena de hasta 100 caracteres).
- `tipo`: Tipo de equipo, que puede ser `weapon` (arma) o `armor` (armadura).
- `potencia`: Un valor entero que representa la potencia del equipo.

###### **Métodos**
Además, cuenta con los siguientes métodos:
- `es_arma()`: Devuelve `True` si el equipo es un arma (`weapon`), `False` en caso contrario.

##### **Modelo `Weapon`**
Este modelo hereda de `Equipment` y representa armas dentro del sistema. Además de los atributos heredados, incluye:

###### **Atributos Principales**
- `alcance`: Un valor entero que representa la distancia de ataque del arma.

##### **Modelo `Armor`**
Este modelo hereda de `Equipment` y representa armaduras dentro del sistema. Además de los atributos heredados, incluye:

###### **Atributos Principales**
- `endurance`: Un valor entero que representa la resistencia de la armadura.

#### **Vistas**

El proyecto cuenta con varias vistas basadas en clases para gestionar el equipamiento y su asignación.

- `EquipmentListView`: Esta vista combina `ListView` y `FormView` para listar el equipo disponible y permitir su asignación a un personaje.
- `AssignEquipmentView`: Vista basada en `FormView` que permite asignar equipo a un personaje. También requiere autenticación.
- `PotenciaView`: Vista basada en `ListView` que muestra una lista de armas cuya potencia es mayor a 30, ordenadas por alcance.
- `AlcanceView`: Lista basada en `ListView` que muestra armas con `alcance` mayor a 5, ordenadas por nombre.

#### **Formulario**
La aplicación utiliza un formulario para la asignación del equipamiento a los personajes del juego.

##### `AssignEquipmentForm`

- **Modelos**: `Character` y `Equipment`
- **Campos**: `character` y `equipment`


### Archivos indispensables para la dockerización del proyecto

Contenido del Dockerfile:
```
# Usa una imagen base ligera de Python
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar paquetes como psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea un usuario para evitar correr la app como root
RUN groupadd -g 1000 django && useradd -m -u 1000 -g django django

# Copia el archivo de dependencias antes de copiar el código (mejora la caché de Docker)
COPY requirements.txt .

# Instala las dependencias de Python globalmente sin usar `--user`
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al contenedor
COPY . .

# Da permisos al usuario para evitar problemas con volúmenes
RUN chown -R django:django /app

# Cambia al usuario no root
USER django
```

Contenido del docker-compose.yml:
```
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django_web
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://postgres:password@db:5432/django_db
      - EMAIL_HOST=mailpit
      - EMAIL_PORT=1025
    depends_on:
      - db
      - mailpit
    command: python manage.py runserver 0.0.0.0:8000
    restart: unless-stopped

  db:
    image: postgres:16
    container_name: postgres_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: django_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  mailpit:
    image: axllent/mailpit
    container_name: mailpit
    volumes:
      - ./data:/data
    ports:
      - "8025:8025"
      - "1025:1025"
    environment:
      MP_MAX_MESSAGES: 5000
      MP_DATABASE: /data/mailpit.db
      MP_SMTP_AUTH_ACCEPT_ANY: 1
      MP_SMTP_AUTH_ALLOW_INSECURE: 1
    restart: unless-stopped

volumes:
  postgres_data:
```

Contenido del requirements.txt:
```
Django==5.1.6
psycopg2==2.9.10
django-debug-toolbar==5.0.1
djangorestframework==3.15.2
sqlparse==0.5.3
tzdata==2025.1
asgiref==3.8.1
```

## Ejemplo de uso
Aquí tienes un enlace al video del ejemplo de uso:
* [Vídeo del ejemplo de uso]()

## Gestión de Trabajo en Equipo
### Parte de cada uno
* Daniel Nogales ha realizado:
  * Los modelos de todas las aplicaciones
  * La app `battle/` 
  * Dockerizar el proyecto
  * API REST
* Dario Romero ha realizado:
  * La app `equipment/`
* Jesús Gómez ha realizado:
  * En la app `character/`
    * Las views: `CreateCharacterView`, `EquipWeaponView`, `ChangeUbicationView`, `RelacionCreateView`
    * Creación de formularios: `CharacterForm` y `RelacionForm` en `forms.py`.
    * Las templates y los css
  * Incluir el LoginRequiredMixin en todas las vistas de todas las aplicaciones del proyecto.
  * La documentación del proyecto: `README.md`

### Pull requests
Estas son todas las pull requests del proyecto:
- [Creación de la app de personaje](https://github.com/daninogales30/juego_tierra_media_django/pull/1)  
- [App equipment](https://github.com/daninogales30/juego_tierra_media_django/pull/2)  
- [App battle](https://github.com/daninogales30/juego_tierra_media_django/pull/3)  
- [App equipment](https://github.com/daninogales30/juego_tierra_media_django/pull/4)  
- [App character](https://github.com/daninogales30/juego_tierra_media_django/pull/5)  
- [README creado](https://github.com/daninogales30/juego_tierra_media_django/pull/6)  
- [Descripción del proyecto](https://github.com/daninogales30/juego_tierra_media_django/pull/7)  
- [App battle](https://github.com/daninogales30/juego_tierra_media_django/pull/8)  
- [He tenido que añadir related_name para diferenciar las relaciones que apuntan a la misma tabla](https://github.com/daninogales30/juego_tierra_media_django/pull/9)  
- [He tenido que añadir related_name para diferenciar las relaciones que apuntan a la misma tabla](https://github.com/daninogales30/juego_tierra_media_django/pull/10)  
- [App battle](https://github.com/daninogales30/juego_tierra_media_django/pull/11)  
- [App character](https://github.com/daninogales30/juego_tierra_media_django/pull/12)  
- [Admin de battle](https://github.com/daninogales30/juego_tierra_media_django/pull/13)  
- [Admin de battle](https://github.com/daninogales30/juego_tierra_media_django/pull/14)  
- [Admin de character](https://github.com/daninogales30/juego_tierra_media_django/pull/15)  
- [Admin de equipment](https://github.com/daninogales30/juego_tierra_media_django/pull/16)  
- [App characters views](https://github.com/daninogales30/juego_tierra_media_django/pull/17)  
- [Vista sobre el StartGameView](https://github.com/daninogales30/juego_tierra_media_django/pull/18)  
- [App characters templates](https://github.com/daninogales30/juego_tierra_media_django/pull/19)  
- [URLs de la app battle y equipment](https://github.com/daninogales30/juego_tierra_media_django/pull/20)  
- [URL de battle modificada](https://github.com/daninogales30/juego_tierra_media_django/pull/21)  
- [Archivo HTML de StartGame](https://github.com/daninogales30/juego_tierra_media_django/pull/22)  
- [URLs](https://github.com/daninogales30/juego_tierra_media_django/pull/23)  
- [Mis vistas hechas, forms.py creado, faltan detalles de personajes y añadir equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/24)  
- [Vista de equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/25)  
- [Manejo de errores](https://github.com/daninogales30/juego_tierra_media_django/pull/26)  
- [App equipment views](https://github.com/daninogales30/juego_tierra_media_django/pull/27)  
- [Cambios en el HttpResponse](https://github.com/daninogales30/juego_tierra_media_django/pull/28)  
- [Views de la app character actualizadas](https://github.com/daninogales30/juego_tierra_media_django/pull/29)  
- [Templates de la app character](https://github.com/daninogales30/juego_tierra_media_django/pull/30)  
- [App characters views](https://github.com/daninogales30/juego_tierra_media_django/pull/31)  
- [Templates creados y modificada la lista de personajes](https://github.com/daninogales30/juego_tierra_media_django/pull/32)  
- [Modificación de vistas de equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/33)  
- [Reverse_lazy modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/34)  
- [DeleteCharacterView modificada](https://github.com/daninogales30/juego_tierra_media_django/pull/35)  
- [Nombre de plantilla crear personaje actualizado](https://github.com/daninogales30/juego_tierra_media_django/pull/36)  
- [App characters templates](https://github.com/daninogales30/juego_tierra_media_django/pull/37)  
- [Start game y CSS hechos](https://github.com/daninogales30/juego_tierra_media_django/pull/38)  
- [He quitado el método de success_url y lo he puesto en la clase directamente](https://github.com/daninogales30/juego_tierra_media_django/pull/39)  
- [App equipment views](https://github.com/daninogales30/juego_tierra_media_django/pull/40)  
- [App equipment views](https://github.com/daninogales30/juego_tierra_media_django/pull/41)  
- [Creación de HTML de equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/42)  
- [Creación de URLs de equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/43): No se subieron los cambios 
- [CSS y HTML lista de personajes creados](https://github.com/daninogales30/juego_tierra_media_django/pull/44)  
- [Página principal modificada](https://github.com/daninogales30/juego_tierra_media_django/pull/45)  
- [Página principal terminada](https://github.com/daninogales30/juego_tierra_media_django/pull/46)  
- [Página con menú de opciones realizada](https://github.com/daninogales30/juego_tierra_media_django/pull/47)  
- [Modificación de clase de equipamiento vista](https://github.com/daninogales30/juego_tierra_media_django/pull/48)  
- [CSS del index y del StartGame](https://github.com/daninogales30/juego_tierra_media_django/pull/49)  
- [Método BattleView creado con HTML](https://github.com/daninogales30/juego_tierra_media_django/pull/50)  
- [BattleView CSS enlazado](https://github.com/daninogales30/juego_tierra_media_django/pull/51)  
- [Creación de templates de equipamiento (no está terminado)](https://github.com/daninogales30/juego_tierra_media_django/pull/52)  
- [CSS formulario crear personaje hecho](https://github.com/daninogales30/juego_tierra_media_django/pull/53)  
- [Modificación de vistas de equipamiento (success_url)](https://github.com/daninogales30/juego_tierra_media_django/pull/54)  
- [App characters CSS](https://github.com/daninogales30/juego_tierra_media_django/pull/55)  
- [Creación de CSS y añadido enlace de los HTMLs](https://github.com/daninogales30/juego_tierra_media_django/pull/56)  
- [BattleView inicio de CSS](https://github.com/daninogales30/juego_tierra_media_django/pull/57)  
- [BattleView CSS completado](https://github.com/daninogales30/juego_tierra_media_django/pull/58)  
- [Eliminación de vistas y reestructuración del equipamiento con forms.py](https://github.com/daninogales30/juego_tierra_media_django/pull/59)  
- [Eliminación de HTMLs y CSS por modificaciones](https://github.com/daninogales30/juego_tierra_media_django/pull/60): No se subieron los cambios
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/61): No se subieron los cambios  
- [Character_detail.css y character_delete.css creados, y character_form.html modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/62)  
- [Modificación de vistas](https://github.com/daninogales30/juego_tierra_media_django/pull/63)  
- [Forms.py modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/64)  
- [Character_detail.html modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/65)  
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/66): No se subieron los cambios  
- [Views.py del character modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/67)  
- [CSS implementado en relacion_form.html](https://github.com/daninogales30/juego_tierra_media_django/pull/68)  
- [Forms.py modificado en las relaciones](https://github.com/daninogales30/juego_tierra_media_django/pull/69)  
- [Login completado](https://github.com/daninogales30/juego_tierra_media_django/pull/70): No se subieron los cambios  
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/71): No se subieron los cambios  