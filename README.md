# 📇 Contact Manager Pro

¡Bienvenido a **Contact Manager Pro**! Una plataforma de nivel empresarial diseñada meticulosamente bajo los fundamentos de **Clean Architecture** (Arquitectura Limpia). Este ecosistema aísla por completo las reglas de negocio core de los frameworks externos, bases de datos e interfaces de usuario, garantizando un producto de software altamente mantenible, escalable y con deuda técnica cero.

El sistema se compone de un robusto **Backend RESTful** auto-documentado y un **Frontend analítico interconectado** que proporciona tableros estadísticos en tiempo real.

---

## 📐 Arquitectura del Sistema

El proyecto implementa un flujo de dependencia unidireccional estricto hacia el centro del dominio (Domain Driven Design), garantizando que las entidades de negocio no dependan de la infraestructura.

```text
    ┌────────────────────────────────────────────────────────┐
    │                       FRONTEND                         │
    │               (Streamlit Dashboard UI)                 │
    └───────────────────────────┬────────────────────────────┘
                                │ (HTTP / REST)
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                       BACKEND                          │
    │         ┌────────────────────────────────────┐         │
    │         │            API ROUTERS             │         │
    │         └─────────────────┬──────────────────┘         │
    │                           ▼                            │
    │         ┌────────────────────────────────────┐         │
    │         │          BUSINESS SERVICES         │         │
    │         └─────────────────┬──────────────────┘         │
    │                           ▼                            │
    │         ┌────────────────────────────────────┐         │
    │         │           DOMAIN MODELS            │         │
    │         └────────────────────────────────────┘         │
    └───────────────────────────┬────────────────────────────┘
                                │ (Abstracción de Storage)
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                  PERSISTENCE LAYER                     │
    │        (JSON Local Storage / Supabase Cloud DB)        │
    └────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías Utilizadas

El stack tecnológico ha sido seleccionado estratégicamente para ofrecer el máximo rendimiento, velocidad de desarrollo y tipado seguro:

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.12 | Base del lenguaje con soporte completo para tipado estático avanzado. |
| **API Framework** | FastAPI | Framework REST de alto rendimiento, asíncrono y auto-documentado bajo OpenAPI. |
| **Frontend UI** | Streamlit | Dashboard interactivo para renderizado analítico de datos y control de formularios. |
| **Gestión de Entornos** | Astral UV | Administrador de paquetes y entornos virtuales ultra-rápido basado en Rust. |
| **Base de Datos Cloud** | Supabase | Capa de persistencia relacional en la nube gestionada a través de PostgreSQL. |
| **Calidad de Código** | Ruff & Radon | Linters de velocidad extrema y evaluadores de complejidad ciclomática de software. |
| **Suite de Testing** | Pytest | Framework robusto para la automatización de pruebas unitarias y de integración. |

---

## 📂 Estructura del Proyecto

La disposición de los directorios refleja el desacoplamiento de responsabilidades dictado por la Arquitectura Limpia:

```text
├── .github/               # Automatizaciones de CI/CD (Calidad de Software y Docs en GitHub)
├── docs/                  # Archivos fuente Markdown de la documentación técnica del sistema
├── src/                   # Código de producción de la aplicación
│   ├── api/               # Capa de adaptadores de red y transporte HTTP (FastAPI)
│   │   ├── routers/       # Enrutadores divididos por contextos lógicos de la API
│   │   ├── config.py      # Gestión centralizada de variables de entorno mediante Pydantic
│   │   └── dependencies.py# Contenedor de inyección de dependencias en caliente
│   ├── frontend/          # Interfaz gráfica de usuario y paneles interactivos
│   │   ├── views/         # Sub-vistas (Directorio analítico, creación y edición)
│   │   └── app.py         # Punto de entrada principal y layouts de Streamlit
│   ├── models/            # Núcleo del Dominio (Entidades puras e Invariantes)
│   │   ├── contact.py     # Agregado raíz del contexto de contactos
│   │   ├── country.py     # Reglas de validación internacional y banderas
│   │   ├── person.py      # Atributos de identidad legal y nombres
│   │   └── number.py      # Estructura e invariantes de formatos telefónicos
│   ├── storage/           # Capa de infraestructura y persistencia (Patrón Repositorio)
│   │   ├── base.py        # Protocolo abstracto e interfaz del repositorio
│   │   ├── json_storage.py# Persistencia en archivos físicos locales estructurados
│   │   └── supabase_storage.py # Conector de infraestructura en la nube
│   ├── exceptions.py      # Excepciones de dominio personalizadas y controladas
│   └── services.py        # Capa de aplicación (Casos de uso y flujos coordinados)
├── mkdocs.yml             # Archivo de configuración global del sitio de documentación
├── pyproject.toml         # Configuración del toolchain unificado (UV, Ruff, Radon, Pytest)
└── tests/                 # Batería de pruebas de software automatizadas
```

---

## ⚙️ Variables de Envorno Necesarias

El sistema cuenta con un gestor inteligente de configuración que altera el comportamiento de almacenamiento sin modificar una sola línea de código. Copia y crea un archivo llamado `.env` en la raíz del proyecto:

```env
# URL base de conexión para el Frontend interactivo
API_URL=http://localhost:8000

# Estrategia de almacenamiento activa: Elige "json" (local) o "supabase" (nube)
STORAGE_STRATEGY=json

# Credenciales Cloud (Requeridas únicamente si STORAGE_STRATEGY=supabase)
SUPABASE_URL=https://tu-id-de-proyecto.supabase.co
SUPABASE_KEY=tu-token-secreto-url-safe-de-supabase
```

---

## 🚀 Instrucciones de Instalación y Ejecución

Asegúrate de tener instalado **Python 3.12** en tu sistema operativo antes de proceder con el despliegue local.

### 1. Clonar el Repositorio e Instalar el Toolchain
Usa la terminal de tu sistema para clonar el proyecto e instalar las dependencias de forma limpia y aislada con `uv`:

```bash
# Clonar el proyecto de software
git clone https://github.com/tu-usuario/Contact_Manager_Full_App.git
cd Contact_Manager_Full_App

# Sincronizar el entorno virtual y descargar dependencias instantáneamente
uv sync
```

### 2. Ejecución del Servidor Backend (FastAPI)
El servidor levantará la API REST y construirá dinámicamente la documentación OpenAPI interactiva:

```bash
# Inicializar el backend en modo desarrollo
uv run fastapi dev src/api/main.py
```
* 💡 **Interacción de la API:** Abre tu navegador web e ingresa a **`http://localhost:8000/docs`** para realizar pruebas de peticiones HTTP directamente desde la interfaz de Swagger.

### 3. Ejecución de la Interfaz Gráfica (Streamlit)
Mantén la terminal del backend corriendo, abre una nueva pestaña en tu terminal y arranca el frontend:

```bash
# Lanzar el dashboard analítico
uv run streamlit run src/frontend/app.py
```
* 🖥️ **Acceso a la App:** El panel se desplegará de forma automática en tu navegador predeterminado bajo la dirección: **`http://localhost:8501`**

---

## 🧪 Suite de Pruebas y Certificación de Calidad

Para mantener el código bajo los máximos estándares de la industria, el proyecto cuenta con herramientas automatizadas de verificación de deuda técnica:

* **Métricas de Complejidad Ciclomática (Radon):** Todo el dominio y los servicios están blindados bajo la **Categoría A** (Código lineal, simple y altamente legible con complejidad inferior a 5).
  ```bash
  uv run radon cc src/api src/models src/storage src/services.py src/exceptions.py -s -n A
  ```

* **Validación de Estilo y Formateador (Ruff):** Comprobación instantánea de buenas prácticas PEP 8 y ordenamiento automático de importaciones.
  ```bash
  uv run ruff check src/
  ```

* **Pruebas Unitarias Cohesionadas (Pytest):** Ejecución instantánea de la suite de pruebas enfocada en validar invariantes de modelos y flujos de servicio:
  ```bash
  uv run pytest
  ```