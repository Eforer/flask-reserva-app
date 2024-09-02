# Informe: Aplicación Web Flask de Reserva de Horas

## 1. Descripción del Proyecto
Desarrollar una aplicación web utilizando el framework Flask de Python para gestionar reservas de horas. La aplicación permitirá a los usuarios registrarse, iniciar sesión, ver disponibilidad de horarios, realizar reservas y administrar sus citas.

## 2. Objetivos
- Crear una interfaz intuitiva para la reserva de horas.
- Implementar un sistema de autenticación de usuarios.
- Desarrollar un panel de administración para gestionar horarios y reservas.
- Asegurar la escalabilidad y mantenibilidad del código.

## 3. Requisitos Funcionales

| Requerimiento | Descripción |
|---------------|-------------|
|RF01 | El sistema debe permitir a los usuarios registrarse con email y contraseña.|
|RF02| Los usuarios deben poder iniciar y cerrar sesión.|
|RF03| El sistema debe mostrar un calendario con las horas disponibles y ocupadas.|
|RF04| Los usuarios deben poder seleccionar una fecha y hora para su reserva.|
|RF05| El sistema debe confirmar las reservas y enviar notificaciones.|
|RF06| Los usuarios deben poder cancelar sus reservas existentes.|
|RF07| El sistema debe enviar recordatorios de las próximas reservas.|
|RF08| Los administradores deben poder gestionar horarios y servicios.|
|RF09| El sistema debe permitir la búsqueda y filtrado de horarios disponibles.|
|RF10| Los usuarios deben poder ver su historial de reservas.|
|RF11| El sistema debe permitir la gestión de perfiles de usuario.|
|RF12| El sistema debe integrar pagos en línea para reservas que lo requieran.|
|RF13| Los usuarios deben poder calificar y dejar comentarios sobre el servicio recibido.|
|RF14| Los administradores deben poder generar reportes sobre el uso del sistema y las reservas.|

## 4. Casos de Uso
| Caso de Uso | Descripción |
|---------------|-------------|
| CU01| Realizar una reserva
| CU02| Cancelar una reserva
| CU03| Gestionar disponibilidad de horarios (Admin)
| CU04| Modificar perfil de usuario
| CU05| Generar reporte de reservas (Admin)

## 5. Historias de Usuario
| Historia | Descripción |
|---------------|-------------|
| HU01| Como usuario, quiero poder registrarme en la aplicación para acceder a los servicios de reserva.
| HU02| Como usuario, quiero ver un calendario con las horas disponibles para poder elegir el momento más conveniente para mi reserva.
| HU03| Como administrador, quiero poder generar reportes de reservas para analizar el uso del sistema.

## 6. Matriz de Trazabilidad
| Requisito | Caso de Uso | Historia de Usuario |
|-----------|-------------|---------------------|
| RF01      | -           | HU01                |
| RF02      | CU01, CU02  | -                   |
| RF03      | CU01        | HU02                |
| RF04      | CU01        | HU02                |
| RF05      | CU01        | -                   |
| RF06      | CU02        | -                   |
| RF07      | -           | -                   |
| RF08      | CU03        | HU03                |
| RF09      | CU01        | HU02                |
| RF10      | CU02        | -                   |

## 7. Tecnologías a Utilizar
- Backend: Flask (Python)
- Base de Datos: MySQL
- ORM: SQLAlchemy
- Frontend: HTML, CSS, JavaScript (posiblemente con un framework como Vue.js)
- Autenticación: Flask-Login
- Formularios: Flask-WTF

## 8. Estructura de la Aplicación
```
/app
    /static
        /css
        /js
    /templates
    /models
    /views
    /forms
    config.py
app.py
requirements.txt
```

## 9. Modelos de Datos
- Usuario
- Reserva
- Servicio (opcional, si se ofrecen diferentes tipos de servicios)

## 10. Rutas Principales
- `/`: Página de inicio
- `/login`: Inicio de sesión
- `/register`: Registro de usuarios
- `/dashboard`: Panel de usuario
- `/reservar`: Página para realizar reservas
- `/admin`: Panel de administración

## 11. Consideraciones de Seguridad
- Utilizar HTTPS
- Implementar protección contra CSRF
- Hashear contraseñas
- Validar y sanitizar entradas de usuario

## 12. Plan de Desarrollo
1. Configuración del entorno y estructura del proyecto
2. Implementación de modelos y base de datos
3. Desarrollo de la autenticación
4. Creación de las vistas principales
5. Implementación de la lógica de reservas
6. Desarrollo del panel de administración
7. Pruebas y depuración
8. Despliegue
