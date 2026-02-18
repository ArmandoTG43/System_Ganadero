# Configuración para PostgreSQL con Docker

## Pasos para configurar:

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar Docker con PostgreSQL
```bash
docker-compose up -d
```

### 3. Migrar la base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 5. Iniciar el servidor
```bash
python manage.py runserver
```

## Conexión con DBeaver

### Datos de conexión:
- **Host**: localhost
- **Puerto**: 5432
- **Base de datos**: ganadero_db
- **Usuario**: ganadero_user
- **Contraseña**: ganadero_password

### Configuración en DBeaver:
1. Abrir DBeaver
2. Click en "New Database Connection"
3. Seleccionar "PostgreSQL"
4. Llenar los datos:
   - Host: localhost
   - Port: 5432
   - Database: ganadero_db
   - User: ganadero_user
   - Password: ganadero_password
5. Click en "Test Connection" para verificar
6. Click en "Finish" para guardar

### PgAdmin (opcional):
- **URL**: http://localhost:5050
- **Email**: admin@ganadero.com
- **Contraseña**: admin123

## Detener Docker
```bash
docker-compose down
```

## Notas:
- Los datos de la base de datos se persisten en Docker
- Puedes acceder a la base de datos directamente con DBeaver
- PgAdmin está disponible para administración web
