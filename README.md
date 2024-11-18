# PopcornHour

## Descripción
Portal web para recomendar, calificar y discutir sobre películas y series.

## Requisitos
- Python 3.11+
- Flask y extensiones (ver `requirements.txt`)

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd PopcornHour

2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt

4. Iniciar la aplicación:
   ```bash
   flask db upgrade
   python run.py

## Uso 
- Registro y autenticación de usuarios.
- Gestión de películas por moderadores
- Calificación y comentarios por usuarios estándar.
