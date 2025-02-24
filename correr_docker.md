## 📌 Pasos para desplegar Django con Docker Compose

### 1️⃣ Asegúrate de que Docker y Docker Compose están instalados
Si no los tienes instalados, puedes verificarlos con:

```bash
docker --version
docker-compose --version
```
Si no están instalados, sigue la guía oficial de instalación.

---

### 2️⃣ Construir y levantar los contenedores
Ejecuta el siguiente comando en la raíz de tu proyecto (donde está `docker-compose.yml`):

```bash
docker-compose up -d --build
```

**Explicación:**
- `-d`: Ejecuta los contenedores en segundo plano (detached mode).
- `--build`: Fuerza la reconstrucción de la imagen en caso de cambios.

---

### 3️⃣ Verificar que los contenedores estén corriendo
Usa el siguiente comando para ver el estado de los contenedores:

```bash
docker ps
```

Debes ver tres contenedores ejecutándose: `django_web`, `postgres_db` y `mailpit`.

Si alguno falló, revisa los logs con:

```bash
docker logs django_web
docker logs postgres_db
```

---

### 4️⃣ Aplicar migraciones y crear superusuario
Ejecuta los siguientes comandos dentro del contenedor de Django:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Esto aplicará las migraciones a la base de datos PostgreSQL y te pedirá un usuario y contraseña para el superusuario.

---

### 5️⃣ Verificar acceso a la aplicación Django
Abre tu navegador y entra a:

- [http://localhost:8000/](http://localhost:8000/) → Debería cargar la aplicación Django.
- [http://localhost:8000/admin/](http://localhost:8000/admin/) → Panel de administración de Django.

Si todo funciona, ya tienes tu aplicación corriendo con Docker 🎉.