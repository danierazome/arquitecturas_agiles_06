# INSTALACION LOCAL PARA REALIZAR EL EXPERIMENTO.
## Instalación y configuración de la base de datos para el experimento (Se debe contar con docker previamente instalado https://www.docker.com/get-started/) además se debe contar con python >= 3.10.12:
- **Descargar posgres y configurarlo:** `docker run --name arquitectura-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=arquitectura -p 5432:5432 -d postgres`
- **Ingresar al contenedor en una terminal:** `docker exec -it arquitectura-postgres bash`
- **Ingresar a la db:** `psql -U user --password password --db arquitectura`
- **Crear tabla *Candidato*:** `CREATE TABLE Candidato (id SERIAL PRIMARY KEY, usuario VARCHAR(60), password VARCHAR(60), nombre VARCHAR(60), experiencia VARCHAR(60), telefono VARCHAR(60), email VARCHAR(60), estado INTEGER);`
- **Crear Candidato:** `INSERT INTO Candidato (usuario, password, nombre, experiencia, telefono, email) VALUES ('test1', '1234', 'test testing', 'Experiencia del Candidato', '123456789', 'correo@valido.com');`
- **Crear CandidatoN2:** `INSERT INTO Candidato (usuario, password, nombre, experiencia, telefono, email) VALUES ('test2', '4321', 'test testing2', 'Experiencia del Candidato2', '1234567890', 'correo@valido.com');`
- **Crear tabla *Empleado*:** `CREATE TABLE Empleado (id SERIAL PRIMARY KEY, usuario VARCHAR(60), password VARCHAR(60));`
- **Crear usuario Empleado:** `INSERT INTO Empleado (usuario, password) VALUES ('empleado1', '6789');`
- **Crear tabla *IntentoFallido*:** `CREATE TABLE intento_fallido (id SERIAL PRIMARY KEY, user_id INTEGER, fecha_intento TIMESTAMP);`

## Instalación y configuración de RabbitMQ:
- **Descargar RabbitMQ:** `docker run -d --hostname arquitectura --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
- La clave por default es guest al igual que el password.

## Configuración EMAIL.
- Para configurar el correo electrónico se debe tener habilidado el servicio de SMTP y IMAP en el servidor.
- Para este experimeto se usa una cuenta de google creada exclusivamente para este propósito: *ssierraoxxonv@gmail.com*
- Si se desea realizar la configuración de otra cuenta de correo, se debe activar el acceso a terceros desde la cuenta de gmail.

# DESPLIEGUE LOCAL.
Para este experimento contamos con 6 microservicios los cuales deben ser desplegados en puertos independientes:
- Activar el VENV para el experimento y ejecutar `pip install -r requirements.txt` de la carpeta raíz del experimento.
- MicroServicio authorization-server: en la carpeta del microservicio correr: `flask run --port 5002`
- MicroServicio block-service: en la carpeta del microservicio correr: `flask run --port 5004`
- MicroServicio candidato-service: en la carpeta del microservicio correr: `flask run --port 5003`
- MicroServicio gateway-service: en la carpeta del microservicio correr: `flask run --port 5000`
- MicroServicio login-service: en la carpeta del microservicio correr: `flask run --port 5001`
- MicroServicio send-email: en la carpeta del microservicio correr: `flask run --port 5005`

# REALIZACIÓN DEL EXPERIMENTO.
En su cliente rest de confianza deberá desarrollar las pruebas necesarias para completar el expermiento; las apis minimas que se deben probar son:
- `POST` *http://localhost:5000/api/login-candidato*
- `GET` *http://localhost:5000/api/candidato?=Bearer token*
- `PUT` *http://localhost:5000/api/candidato*
- `POST` *http://localhost:5000/api/login-empleado*
- `GET` *http://localhost:5000/api/candidato*