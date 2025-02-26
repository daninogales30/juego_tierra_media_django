# Juego Tierra Media con Django

## Descripción del proyecto
Este proyecto es una implementación del Juego Tierra Media utilizando 
Django, un framework de Python de alto nivel especializado en el 
desarrollo web, API REST y dockerizandola con Docker. El permite gestionar diferentes aspectos 
del juego mediante una interfaz web.

Cada aplicación tiene distintas funcionalidades relacionadas al nombre de la aplicación:
* En la app `Battle`, puedes simular un enfrentamiento entre 2 personajes para ver quién ganaría.
* La aplicación `Character` te permite crear personajes, gestionarlos y ver los detalles de cada uno. Puedes 
ver el listado de personajes, filtrarlos para ver cuales son de la raza humana, cuales tienen armas, etc.
* La aplicación `Equipment` permite tener armas que les puede añadir al inventario de los 
diferentes personajes y equipárselas, ver sus estadísticas (Potencia y Alcance), listar las armas 
con más su alcance o potencia.

## Estructura del Proyecto
Para comprender bien el funcionamiento del proyecto, una de las cosas que hay que 
saber como es la estructura del proyecto. 
A continuación, veremos el árbol de archivos y directorios de este proyecto.
```
├── templates/        # Plantillas del login y registro
├── juego_tierra_media_django/  # Carpeta principal
│   ├── settings.py   # Configuración del proyecto
│   └── urls.py       # Rutas a las diferentes aplicaciones del proyecto, 
│                       al admin y para logear o registrar un usuario
├── requirements.txt  
├── manage.py         
├── docker-compose.yml
├── Dockerfile
├── README.md         # Documentación del proyecto (este archivo)
├── battle/           # App de batallas
│   ├── models.py     # Modelo para batalla
│   ├── views.py      # Vistas de la aplicación
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

### APLICACIÓN `battle/`
#### **Modelos**
##### **Modelo `Battle`**
Simula una batalla entre dos personajes y muestra la información sobre el resultado.
###### **Atributos Principales**
- `character1`: Primer personaje en la batalla (relación con `Character`).
- `character2`: Segundo personaje en la batalla (relación con `Character`).
- `winner`: Personaje ganador de la batalla (puede ser `null` si aún no se ha determinado).
- `loser`: Personaje perdedor de la batalla (puede ser `null` si aún no se ha determinado).
- `date`: Fecha y hora en la que se creó la batalla.

###### **Métodos Principales**
- `simulate()`:Este método simula la batalla entre `character1` y `character2` siguiendo las siguientes reglas:
    1. **Verificación de armas**: Ambos personajes deben tener un arma equipada para pelear.
    2. **Inicialización de valores**:
       - Se obtiene la vida máxima de ambos personajes.
       - Se establece la resistencia (`stamina`) inicial en 100 para ambos.
       - Se define una probabilidad base de golpe crítico (`critico = 0.10`).
    3. **Ciclo de combate**:
       - En cada ronda, `character1` ataca a `character2`, reduciendo su vida.
       - Si `character2` sigue con vida, ataca a `character1`.
       - Se reduce la resistencia del atacante en cada turno.
       - El combate se detiene si uno de los personajes queda sin vida o se alcanzan 20 rondas.
    4. **Determinación del ganador**:
       - El personaje con vida restante es el ganador.
       - Si ambos personajes caen al mismo tiempo, el ganador se elige aleatoriamente.
       - El ganador conserva el 30% de su vida máxima y el perdedor queda con 0 de vida.
- `calculate_damage(attacker, stamina, base_crit)`:Calcula el daño infligido por un personaje considerando los siguientes factores:
    - **Potencia del arma equipada**.
    - **Probabilidad de golpe crítico**, modificada por la resistencia (`stamina`) y un factor de suerte (`suerte`).
    - **Multiplicador de crítico**: Si el ataque es crítico, el daño se multiplica por `2.5`.
    - **Rango de daño**: Se calcula entre el 80% y el 120% de la potencia base.

#### **Vistas**
##### `BattleView`
Se encarga de validar y procesar la batalla:

1. **Obtiene los personajes**: 
   - `jugador1` y `jugador2` son los personajes seleccionados en el formulario.

2. **Validaciones previas**:
   - Se impide que un personaje pelee contra sí mismo.
   - Ambos personajes deben tener un arma equipada.

3. **Creación y simulación de la batalla**:
   - Se crea una instancia del modelo `Battle` con los personajes seleccionados.
   - Se ejecuta el método `simulate()` para llevar a cabo el combate.
   - Si ocurre un error durante la simulación, se agrega un mensaje de error al formulario.

4. **Renderización de la plantilla**:
   - Se pasa la información de la batalla al contexto del template, incluyendo:
     - `battle`: Instancia de la batalla simulada.
     - `character1` y `character2`: Los personajes en combate.
     - `loser`: Personaje que ha perdido la batalla.

#### Formularios
`BattleForm`: recoge los datos de los 2 personajes que van a luchar en la simulación de la batalla.

#### **Tests**
```
class BattleViewTest(TestCase):
    def setUp(self):
        self.weapon = Weapon.objects.create(name="Espada", damage=10)
        self.character1 = Character.objects.create(name="Guerrero", health=100)
        self.character2 = Character.objects.create(name="Mago", health=100)
        self.character1.arma_equipada = self.weapon
        self.character2.arma_equipada = self.weapon
        self.character1.save()
        self.character2.save()

    def test_battle_view_loads(self):
        response = self.client.get(reverse("battle:battle_view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "battleview.html")

    def test_cannot_fight_self(self):
        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character1.id
        })
        self.assertFormError(response, "form", "jugador1", "No se puede pelear con el mismo personaje")

    def test_cannot_fight_without_weapon(self):
        self.character2.arma_equipada = None
        self.character2.save()

        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character2.id
        })
        self.assertFormError(response, "form", "jugador1", "Se necesita equipar un arma en ambos personajes")

    def test_successful_battle(self):
        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character2.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("ganador", response.context)
        self.assertTrue(Battle.objects.exists())

```

### APLICACIÓN `character/`
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

#### **Vistas ORM**
- `HumanosView`: Vista para listar personajes de la raza humana.
- `HumanosSinArmaView`: Vista para listar personajes humanos sin arma equipada.

#### **Vistas API REST**
- `RelacionViewSet`: Endpoints para gestionar relaciones entre personajes.
- `CharacterViewSet`: Endpoints para gestionar personajes con filtrado por nombre y facción.

#### **Formularios**
La aplicación utiliza formularios de Django para la creación y actualización relacionados con personajes y relaciones:

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

#### **Tests**
```
class EquipmentModelTest(TestCase):

    def test_equipment_creation(self):

        equipment = Equipment.objects.create(
            name="Espada",
            tipo="weapon",
            potencia=10
        )
        self.assertEqual(equipment.name, "Espada")
        self.assertEqual(equipment.tipo, "weapon")
        self.assertEqual(equipment.potencia, 10)
        self.assertTrue(equipment.es_arma())

    def test_equipment_str_method(self):

        equipment = Equipment.objects.create(
            name="Escudo",
            tipo="armor",
            potencia=5
        )
        self.assertEqual(str(equipment), "Escudo")

    def test_equipment_tipo_choices(self):

        equipment = Equipment.objects.create(
            name="Lanza",
            tipo="weapon",
            potencia=7
        )
        self.assertIn(equipment.tipo, [choice[0] for choice in Equipment._meta.get_field('tipo').choices])


        with self.assertRaises(ValueError):
            Equipment.objects.create(
                name="Poción",
                tipo="potion",  # Tipo inválido
                potencia=2
            )

    def test_equipment_unique_name(self):

        Equipment.objects.create(
            name="Espada",
            tipo="weapon",
            potencia=10
        )
        with self.assertRaises(Exception):
            Equipment.objects.create(
                name="Espada",
                tipo="armor",
                potencia=5
            )


class WeaponModelTest(TestCase):

    def test_weapon_creation(self):

        weapon = Weapon.objects.create(
            name="Arco",
            tipo="weapon",
            potencia=8,
            alcance=100
        )
        self.assertEqual(weapon.name, "Arco")
        self.assertEqual(weapon.tipo, "weapon")
        self.assertEqual(weapon.potencia, 8)
        self.assertEqual(weapon.alcance, 100)
        self.assertTrue(weapon.es_arma())

    def test_weapon_inheritance(self):

        weapon = Weapon.objects.create(
            name="Hacha",
            tipo="weapon",
            potencia=12,
            alcance=50
        )
        self.assertIsInstance(weapon, Equipment)



class CharacterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character = Character.objects.create(name='Hero', owner=self.user)

    def test_create_character_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('character:create_character'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'character_form.html')

    def test_character_list_view(self):
        response = self.client.get(reverse('character:character_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero')

    def test_delete_character_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:delete_character', args=[self.character.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Character.objects.filter(id=self.character.id).exists())

class EquipWeaponTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character = Character.objects.create(name='Hero', owner=self.user)

    def test_equip_weapon(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:equip_weapon', args=[self.character.id]),
                                    {'arma_equipada': 'Espada'})
        self.character.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.character.arma_equipada, 'Espada')

class RelacionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character1 = Character.objects.create(name='Hero', owner=self.user)
        self.character2 = Character.objects.create(name='Villain', owner=self.user)

    def test_create_relacion(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:create_relacion'), {
            'character1': self.character1.id,
            'character2': self.character2.id,
            'relation_type': 'enemigo'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Relacion.objects.filter(character1=self.character1, character2=self.character2).exists())
```

### APLICACIÓN `equipment/`
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

#### **Vistas ORM**

- `PotenciaView`: Vista basada en `ListView` que muestra una lista de armas cuya potencia es mayor a 30, ordenadas por alcance.
- `AlcanceView`: Lista basada en `ListView` que muestra armas con `alcance` mayor a 5, ordenadas por nombre.

#### **Formulario**
`AssignEquipmentForm`: asignación del equipamiento a los personajes del juego.

#### **Tests**
```
class EquipmentModelTest(TestCase):

    def test_equipment_creation(self):
        equipment = Equipment.objects.create(
            name="Espada",
            tipo="weapon",
            potencia=10
        )
        self.assertEqual(equipment.name, "Espada")
        self.assertEqual(equipment.tipo, "weapon")
        self.assertEqual(equipment.potencia, 10)
        self.assertTrue(equipment.es_arma())

    def test_equipment_str_method(self):
        equipment = Equipment.objects.create(
            name="Escudo",
            tipo="armor",
            potencia=5
        )
        self.assertEqual(str(equipment), "Escudo")

class WeaponModelTest(TestCase):

    def test_weapon_creation(self):
        weapon = Weapon.objects.create(
            name="Arco",
            tipo="weapon",
            potencia=8,
            alcance=100
        )

        self.assertEqual(weapon.name, "Arco")
        self.assertEqual(weapon.tipo, "weapon")
        self.assertEqual(weapon.potencia, 8)
        self.assertEqual(weapon.alcance, 100)
        self.assertTrue(weapon.es_arma())
class EquipmentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        cls.character = Character.objects.create(name='Test Character')
        cls.equipment = Equipment.objects.create(name='Sword')

    def test_equipment_list_view(self):
        response = self.client.get(reverse('equipment:equipment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment_list.html')
        self.assertContains(response, self.equipment.name)

    def test_assign_equipment_view_get(self):
        response = self.client.get(reverse('equipment:assign_equipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assign_equipment.html')

    def test_assign_equipment_view_post(self):
        response = self.client.post(reverse('equipment:assign_equipment'), {
            'character': self.character.id,
            'equipment': self.equipment.id
        })
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertIn(self.equipment, self.character.equipment.all())
```

### Archivos indispensables para la dockerización del proyecto

Contenido del `Dockerfile`:
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

Contenido del `docker-compose.yml`:
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

Contenido del `requirements.txt`:
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
* [Vídeo del ejemplo de uso](https://www.youtube.com/watch?v=uSiIE0iz7QI)

## Gestión de Trabajo en Equipo
### Parte de cada uno
* Daniel Nogales ha realizado:
  - Los modelos de todas las aplicaciones
  - Las views, el `forms.py` las templates y la hoja de estilos de `battle/`
  - Las armas precargadas de `signals.py`
  - Dockerizar el proyecto
  - API REST
  - La corrección de errores en el proyecto
* Dario Romero ha realizado:
  - En la app `character/`:
    - El ORM con las views `HumanosView` y `HumanosSinArmaView`
    - Las vistas `DeleteCharacterView`, `DetailCharacterView` y `CharacterListView` de la app `character/`
  - En la app `equipment`:
    - El ORM con las views `PotenciaView` y `AlcanceView`
    - Las vistas, el `forms.py`, las templates y las hojas de estilos de la app `equipment/`
  - La Debug Toolbar
  - El admin y los tests de todas las aplicaciones.
* Jesús Gómez ha realizado:
  - En la app `character/`:
    - Las views: `CreateCharacterView`, `EquipWeaponView`, `ChangeUbicationView`, `RelacionCreateView`
    - Creación de formularios: `CharacterForm` y `RelacionForm` en `forms.py`
    - Las templates y las hojas de estilos
  - Incluir el LoginRequiredMixin en varias de las vistas de todas las aplicaciones del proyecto
  - La documentación del proyecto: `README.md`

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
- [Character_detail.css y character_delete.css creados, y character_form.html modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/62)  
- [Modificación de vistas](https://github.com/daninogales30/juego_tierra_media_django/pull/63)  
- [Forms.py modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/64)  
- [Character_detail.html modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/65)
- [Views.py del character modificado](https://github.com/daninogales30/juego_tierra_media_django/pull/67)  
- [CSS implementado en relacion_form.html](https://github.com/daninogales30/juego_tierra_media_django/pull/68)  
- [Forms.py modificado en las relaciones](https://github.com/daninogales30/juego_tierra_media_django/pull/69)
- [README.md actualizado](https://github.com/daninogales30/juego_tierra_media_django/pull/72)
- [README.md actualizado otra vez](https://github.com/daninogales30/juego_tierra_media_django/pull/723)

Estas son las pull requests cuyos cambios no se subieron:
- [Creación de URLs de equipamiento](https://github.com/daninogales30/juego_tierra_media_django/pull/43): No se subieron los cambios
- [Eliminación de HTMLs y CSS por modificaciones](https://github.com/daninogales30/juego_tierra_media_django/pull/60): No se subieron los cambios
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/61): No se subieron los cambios 
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/66): No se subieron los cambios
- [Login completado](https://github.com/daninogales30/juego_tierra_media_django/pull/70): No se subieron los cambios
- [App equipment templates](https://github.com/daninogales30/juego_tierra_media_django/pull/71): No se subieron los cambios