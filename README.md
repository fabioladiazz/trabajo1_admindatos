# Pipeline de Procesamiento de Datos y Machine Learning
Fabiola Díaz, Valerie Espinoza y Alejandro Ocampo
## Requisitos Previos
Antes de ejecutar el pipeline, asegúrate de cumplir con los siguientes requisitos:

1. **Archivo de credenciales de Kaggle:** Debes contar con un archivo `kaggle.json` generado desde tu cuenta de Kaggle. Si no lo tienes, puedes generarlo en [Kaggle API](https://www.kaggle.com/docs/api).
2. **Dependencias Instaladas:**
   - Python 3.x
   - Kaggle API
   - Librerías necesarias (puedes instalarlas con `pip install -r requirements.txt`)
3. **Acceso y credenciales del sistema:**
   - `admin` (Acceso completo) → **Usuario:** `acceso1`
   - `analyst` (Solo lectura) → **Usuario:** `acceso2`
   - `guest` (Acceso restringido) → **Usuario:** `acceso3`

---

## Flujo de Trabajo del Pipeline
El pipeline sigue estos pasos de ejecución:

### **1 Autenticación de Usuario**
- Se solicita al usuario ingresar su nombre y contraseña.
- Se verifica que las credenciales sean correctas y que el usuario tenga permisos suficientes para continuar.
- Si la autenticación falla, el acceso se bloquea.

### **2 Extracción de Datos**
- Se conecta a Kaggle utilizando las credenciales almacenadas en `kaggle.json`.
- Se descarga un conjunto de datos específico y se extrae para su uso posterior.

### **3 Encriptación y Respaldo**
- Antes de modificar los datos, se genera una copia de seguridad.
- Se encriptan los datos para proteger la privacidad y se almacenan en un archivo seguro.

### **4 Procesamiento de Datos**
- Los datos encriptados se desencriptan temporalmente para su procesamiento.
- Se guardan en un archivo accesible solo durante la ejecución del pipeline.

### **5 Entrenamiento del Modelo**
- Se ejecuta un notebook de Jupyter que entrena un modelo de machine learning con los datos procesados.
- Tras finalizar, el archivo desencriptado se elimina automáticamente para mantener la seguridad.
- Se verifica que el modelo (`modelo_final.pkl`) se haya generado correctamente.

### **6 Almacenamiento en la Nube**
- Si el pipeline se completa con éxito:
  - Se suben automáticamente los cambios al repositorio de GitHub.
  - Se eliminan archivos temporales innecesarios (`modelo.nbconvert.ipynb`).
  - Se registra un historial de acciones en `audit_log.txt`.

---

## ▶ **Cómo Ejecutar el Script**
Sigue estos pasos para ejecutar el pipeline correctamente:

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/usuario/repositorio.git
   cd repositorio
   ```

2. Coloca el archivo `kaggle.json` en la carpeta adecuada:
   - Para Mac/Linux:
     ```bash
     mkdir -p ~/.kaggle
     mv kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json
     ```
   - Para Windows:
     ```powershell
     mkdir C:\Users\tu_usuario\.kaggle
     Move-Item kaggle.json C:\Users\tu_usuario\.kaggle\
     ```

3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el script principal:
   ```bash
   python main.py
   ```

5. Ingresa tu usuario y contraseña cuando se te solicite.
   - Recibirás un mensaje indicando si la autenticación fue exitosa.

6. Verifica los resultados:
   - El pipeline se ejecutará automáticamente.
   - Se realizará un `push` a GitHub.
   - Revisa los registros en `audit_log.txt` para validar el proceso.

---

## Notas Adicionales
- Si tienes problemas con la ejecución, revisa los permisos del archivo `kaggle.json`.
- Si necesitas más información sobre cómo utilizar Kaggle API, consulta la [documentación oficial](https://www.kaggle.com/docs/api).

---