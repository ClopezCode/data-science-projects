# Predicción de Precios con Regresión Lineal 📈

Este proyecto utiliza datos históricos de precios de acciones de AAPL para entrenar un modelo de regresión lineal que realiza una predicción básica del precio de cierre del día siguiente.

---

## 📝 Descripción

El proyecto tiene los siguientes objetivos:

1. Descargar datos históricos de acciones utilizando la librería `yfinance`.
2. Preparar y limpiar los datos para su uso en un modelo predictivo.
3. Entrenar un modelo de regresión lineal que predice el precio de cierre del día siguiente.
4. Evaluar el modelo utilizando el **Error Cuadrático Medio (MSE)** como métrica de desempeño.

**Nota:** Este modelo es simple y utiliza solo el precio de cierre como única característica predictiva. No es una herramienta de predicción financiera avanzada.

---

## 🛠️ Herramientas y Tecnologías

- **Lenguaje:** Python 3.8+
- **Librerías:**
  - `yfinance`: Para descargar los datos históricos.
  - `pandas`: Manipulación de datos.
  - `numpy`: Operaciones matemáticas.
  - `scikit-learn`: Creación y evaluación del modelo de regresión.
  - `joblib`: Guardar y cargar el modelo entrenado.
  - `matplotlib` (opcional): Visualización de datos.

---

## 📂 Estructura del Proyecto

```plaintext
prediccion-precios/
├── data/
│   └── AAPL.csv          # Archivo con los datos históricos de AAPL
├── model/
│   └── linear_regression_model.pkl  # Modelo entrenado de regresión lineal
├── notebooks/            # (Opcional) Notebooks para exploración
├── scripts/
│   ├── download_data.py  # Descarga datos históricos de AAPL
│   ├── prepare_data.py   # Limpia y prepara los datos
│   └── train_model.py    # Entrena y evalúa el modelo
├── README.md             # Documentación del proyecto
└── requirements.txt      # Dependencias del proyecto
```
---

## 🚀 Cómo Ejecutar el Proyecto
- Crear un entorno virtual: 
python -m venv venv
- Activar el entorno virtual: venv\Scripts\activate
- Instalar las dependencias: pip install -r requirements.txt
- Ejecutar los scripts:
- Descargar datos: python scripts/download_data.py
- Preparar datos: python scripts/prepare_data.py
- Entrenar el modelo: python scripts/train_model.py
