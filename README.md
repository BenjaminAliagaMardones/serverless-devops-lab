# DevOps Lab — API Serverless en AWS con Terraform y Docker

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=aws-lambda&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

Laboratorio práctico para aprender y experimentar con despliegues serverless en AWS. Una API construida con FastAPI se empaqueta en un contenedor Docker, se despliega como función Lambda, y toda la infraestructura se gestiona con Terraform y CI/CD automatizado mediante GitHub Actions.

---

## 📐 Arquitectura Serverless (Lambda + Docker)

Tradicionalmente, las funciones AWS Lambda se despliegan utilizando archivos `.zip` con el código y las dependencias. Sin embargo, para simplificar el despliegue de frameworks web como FastAPI y manejar dependencias pesadas, este proyecto utiliza la modalidad de **Imágenes de Contenedor para AWS Lambda**:

1. **Dockerización:** La aplicación FastAPI y todas sus dependencias de Python se empaquetan en una imagen Docker estándar usando un `Dockerfile`.
2. **Registro de Contenedores (AWS ECR):** Terraform aprovisiona un repositorio en **AWS Elastic Container Registry (ECR)**.
3. **Flujo de Publicación (CI/CD):** La imagen Docker construida se sube (push) al repositorio ECR.
4. **AWS Lambda:** La función Lambda se configura para ejecutarse a partir de la imagen almacenada en ECR.
5. **Adaptador Lambda (AWS Lambda Web Adapter / Mangum):**
   * *Opción recomendada (sin cambios de código):* Se puede utilizar el **AWS Lambda Web Adapter** dentro del Dockerfile, el cual actúa como un proxy inverso que traduce las solicitudes de API Gateway o Lambda Function URLs en peticiones HTTP estándar de FastAPI corriendo en el puerto 8000.
   * *Opción ASGI (Mangum):* Utilizar la librería `mangum` en Python para envolver la aplicación FastAPI y definir un manejador (handler) compatible con Lambda.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11)
- **Adaptador Serverless:** [Mangum](https://mangum.io/) o [AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)
- **Base de Datos:** [PostgreSQL](https://www.postgresql.org/) con [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- **Contenedores:** [Docker](https://www.docker.com/) (Dockerfile optimizado para AWS Lambda)
- **Infraestructura como Código (IaC):** [Terraform](https://www.terraform.io/) (gestionando AWS ECR y la función Lambda)
- **Automatización & Configuración:** [Ansible](https://www.ansible.com/)
- **CI/CD:** [GitHub Actions](https://github.com/features/actions)
- **Proveedor Cloud:** [Amazon Web Services (AWS)](https://aws.amazon.com/)

---

## 📁 Estructura del Proyecto

```text
├── .github/
│   └── workflows/
│       ├── terraform-ci.yml   # CI/CD: Valida y aplica la infraestructura en AWS (rama main)
│       └── destroy.yml        # CD: Destruye los recursos de Terraform de forma manual
├── ansible/                   # Playbooks e inventarios de Ansible para configuración de entornos
├── app/                       # Código fuente de la aplicación FastAPI
│   ├── app.py                 # Puntos de entrada y lógica de rutas de FastAPI
│   ├── database.py            # Configuración de la conexión a PostgreSQL con SQLAlchemy
│   ├── dockerfile             # Receta para construir la imagen Docker compatible con Lambda
│   ├── models.py              # Definición del modelo de datos de Visitas
│   └── requirements.txt       # Dependencias de Python (FastAPI, uvicorn, psycopg2-binary, etc.)
├── terraform/                 # Archivos de configuración de Terraform
│   └── main.tf                # Definición de recursos (AWS ECR para alojar la imagen de Lambda)
└── README.md                  # Descripción detallada del proyecto
```

---

## 🚀 Componentes del Proyecto

### 1. Aplicación FastAPI (`/app`)
Una API sencilla que expone un endpoint raíz (`/`). Al recibir una solicitud:
1. Incrementa un contador de visitas almacenado en la tabla `visitas` de PostgreSQL.
2. Devuelve un saludo de bienvenida orientando el laboratorio y el número acumulado de visitas en formato JSON:
   ```json
   {
     "mensaje": "Bienvenido a mi lab con AWS, Docker, Terraform y Ansible",
     "vistas": 42
   }
   ```

### 2. Infraestructura con Terraform (`/terraform`)
Utiliza Terraform para crear de manera declarativa los recursos necesarios en AWS.
- Configura un registro de contenedores en **AWS Elastic Container Registry (ECR)** llamado `mi-app-lambda` para almacenar las imágenes Docker de la función Lambda.

### 3. Pipeline de CI/CD (`.github/workflows`)
- **Terraform CI/CD (`terraform-ci.yml`)**: Se ejecuta automáticamente ante cada `push` o `pull_request` a la rama `main`. Valida el formato (`terraform fmt`), inicializa el proveedor (`terraform init`), muestra la planificación (`terraform plan`) y aplica los cambios (`terraform apply`) al fusionarse en `main`.
- **Terraform Destroy (`destroy.yml`)**: Permite destruir manualmente toda la infraestructura creada directamente desde la pestaña Actions de GitHub.

---

## 💻 Desarrollo Local y Pruebas

### Requisitos Previos
- Python 3.11+ instalado
- PostgreSQL corriendo localmente o en un contenedor Docker
- Docker instalado

### Configuración del Entorno local (Python)
1. Crea y activa un entorno virtual de Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # o
   venv\Scripts\activate     # En Windows
   ```
2. Instala las dependencias:
   ```bash
   pip install -r app/requirements.txt
   ```
3. Configura las variables de entorno necesarias para la base de datos (puedes definirlas temporalmente en tu terminal):
   ```bash
   export DB_USER="postgres"
   export DB_PASSWORD="tu_password"
   export DB_HOST="localhost"
   export DB_PORT="5432"
   export DB_NAME="mydb"
   ```
4. Ejecuta la aplicación usando `uvicorn` desde la raíz del proyecto:
   ```bash
   uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
   ```
   La aplicación estará disponible en `http://localhost:8000`.

### Construcción y Ejecución Local del Contenedor Lambda
Puedes empaquetar y ejecutar la aplicación dentro del contenedor Docker localmente para simular el comportamiento en la nube.

1. Construye la imagen de Docker:
   ```bash
   docker build -t mi-app-lambda -f app/dockerfile app/
   ```
2. Ejecuta el contenedor, asegurándote de inyectar las variables de entorno correctas para conectar con tu base de datos:
   ```bash
   docker run -d -p 8000:8000 \
     -e DB_USER="postgres" \
     -e DB_PASSWORD="tu_password" \
     -e DB_HOST="host.docker.internal" \
     -e DB_PORT="5432" \
     -e DB_NAME="mydb" \
     mi-app-lambda
   ```

---

## ☁️ Configuración en Producción y GitHub Actions

Para habilitar el despliegue automático a través de GitHub Actions:

1. Ve a la configuración de tu repositorio en GitHub (`Settings` -> `Secrets and variables` -> `Actions`).
2. Añade los siguientes **Repository secrets**:
   - `AWS_ACCESS_KEY_ID`: Tu ID de clave de acceso de AWS.
   - `AWS_SECRET_ACCESS_KEY`: Tu clave secreta de acceso de AWS.
3. El pipeline compilará la imagen usando el `dockerfile`, la subirá al repositorio ECR creado por Terraform, y actualizará la función Lambda para que apunte a la última versión de la imagen en ECR.
