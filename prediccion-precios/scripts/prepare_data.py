import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_prepare_data(file_path):
    """
    Carga y prepara los datos históricos para el modelo de predicción.
    """
    # Cargar datos
    data = pd.read_csv(file_path, parse_dates=["Date"])
    data.set_index("Date", inplace=True)
    print("Primeras filas del dataset cargado:")
    print(data.head())

    # Seleccionar características
    data["Target"] = data["Close"].shift(-1)  # Predicción del siguiente día
    data.dropna(inplace=True)  # Eliminar valores nulos generados por el shift

    # Filtrar solo columnas numéricas
    data = data.apply(pd.to_numeric, errors='coerce')
    data.dropna(inplace=True)  # Eliminar filas con valores no numéricos
    print("Dataset después de filtrar valores no numéricos:")
    print(data.head())

    # Dividir en características (X) y objetivo (y)
    X = data[["Close"]]
    y = data["Target"]

    # Verificación de los datos
    print("Verificando que X solo contenga valores numéricos:")
    print(X.dtypes)
    print("Primeras filas de X:")
    print(X.head())
    
    print("Verificando que y solo contenga valores numéricos:")
    print(y.dtypes)
    print("Primeras filas de y:")
    print(y.head())

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Ruta al archivo de datos
    file_path = "prediccion-precios/data/AAPL.csv"

    # Preparar datos
    X_train, X_test, y_train, y_test = load_and_prepare_data(file_path)
    print("Datos preparados exitosamente")
