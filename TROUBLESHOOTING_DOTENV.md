# 🔧 Guía de Solución: Error "dotenv could not be resolved"

**Problema:** Pylance reporta que el import `from dotenv import load_dotenv` no puede ser resuelto.

**Causa:** El paquete `python-dotenv` no está instalado en el entorno Python actual.

---

## ✅ Soluciones Rápidas

### Opción 1: Script Automático (Recomendado)

```bash
# En la raíz del proyecto
python install_deps.py
```

Esto automáticamente:
- Actualiza pip
- Instala todas las dependencias de requirements.txt
- Verifica que python-dotenv esté correctamente instalado
- Te da instrucciones para recargar Pylance en VS Code

---

### Opción 2: Instalación Manual

#### Windows
```cmd
# Activar venv si existe
venv\Scripts\activate.bat

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar python-dotenv
pip show python-dotenv
```

#### Linux / macOS
```bash
# Activar venv si existe
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar python-dotenv
pip show python-dotenv
```

---

### Opción 3: Solo Instalar python-dotenv

```bash
pip install python-dotenv==1.0.0
```

---

## 🔄 Recargar Pylance en VS Code

Después de instalar, sigue estos pasos:

### Paso 1: Seleccionar el Intérprete Correcto

1. Presiona `Ctrl+Shift+P` (Windows/Linux) o `Cmd+Shift+P` (Mac)
2. Escribe: `Python: Select Interpreter`
3. Elige el intérprete del venv actual (si creaste uno) o el intérprete del sistema

### Paso 2: Recargar VS Code

Opción A - Desde la paleta de comandos:
1. `Ctrl+Shift+P`
2. Escribe: `Developer: Reload Window`
3. Presiona Enter

Opción B - Manualmente:
- File → Reload Window
- O presiona `Ctrl+R`

### Paso 3: Verificar

El error debería desaparecer. Si persiste:
- Cierra la carpeta del proyecto
- Reabre la carpeta
- VS Code reconstruirá el índice de Pylance

---

## 🛡️ Mejora Realizada en settings.py

**Antes (causaba error):**
```python
from dotenv import load_dotenv
load_dotenv()
```

**Ahora (es robusto):**
```python
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv no instalado, usa variables de entorno del sistema
    pass
```

Esto permite que el proyecto funcione incluso sin `python-dotenv` instalado, y solo intenta cargar el archivo `.env` si el paquete está disponible.

---

## ✨ Verificación

Para confirmar que todo está instalado correctamente:

```bash
# Verificar que los paquetes principales están instalados
python -c "import django; print(f'Django {django.__version__}')"
python -c "import rest_framework; print(f'DRF {rest_framework.__version__}')"
python -c "import dotenv; print(f'python-dotenv {dotenv.__version__}')"

# Resultado esperado:
# Django 5.0.1
# DRF 3.14.0
# python-dotenv 1.0.0
```

---

## 🚀 Si Aún Tienes Problemas

### 1. Verificar la ruta de requirements.txt
```bash
# Desde la raíz del proyecto
cat requirements.txt

# Debe mostrar la lista de dependencias incluyendo python-dotenv
```

### 2. Reinstalar todo desde cero

```bash
# Limpiar pip cache
pip cache purge

# Reinstalar
pip install -r requirements.txt --no-cache-dir
```

### 3. Crear un nuevo venv

```bash
# Windows
python -m venv venv_new
venv_new\Scripts\activate.bat
pip install -r requirements.txt

# Linux/macOS
python3 -m venv venv_new
source venv_new/bin/activate
pip install -r requirements.txt
```

### 4. Verificar VS Code está usando el venv correcto

En VS Code:
- Abre la terminal integrada: `` Ctrl+` ``
- Debe mostrar `(venv)` o `(venv_new)` al inicio
- Si no, haz click en el intérprete Python en la esquina inferior derecha

---

## 📋 Checklist

- [ ] Ejecuté `python install_deps.py` o `pip install -r requirements.txt`
- [ ] Ejecuté `pip show python-dotenv` y confirmé que está instalado
- [ ] Seleccioné el intérprete correcto en VS Code
- [ ] Recargué VS Code (Ctrl+R)
- [ ] El error de Pylance desapareció
- [ ] Los imports en settings.py están resueltos

---

## 📚 Archivos Relacionados

- [requirements.txt](requirements.txt) - Lista de dependencias
- [config/settings.py](config/settings.py) - Configuración Django (ahora con try-except)
- [install_deps.py](install_deps.py) - Script de instalación automática
- [QUICK_START.md](QUICK_START.md) - Guía rápida de inicio
- [INSTALL.md](INSTALL.md) - Instalación detallada

---

**Última actualización:** Febrero 28, 2026
**Estado:** ✅ Resuelto
