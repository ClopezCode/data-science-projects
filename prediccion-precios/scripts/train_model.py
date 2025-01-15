import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from prepare_data import load_and_prepare_data

def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    """
    Entrena un modelo de regresión lineal y evalúa su rendimiento.
    """
    # Crear el modelo
    model = LinearRegression()

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Evaluar el modelo
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Error cuadrático medio (MSE): {mse}")

    # Guardar el modelo entrenado
    joblib.dump(model, "prediccion-precios/model/linear_regression_model.pkl")
    print("Modelo guardado exitosamente")

if __name__ == "__main__":
    # Preparar datos
    file_path = "prediccion-precios/data/AAPL.csv"
    X_train, X_test, y_train, y_test = load_and_prepare_data(file_path)

    # Entrenar y evaluar el modelo
    train_and_evaluate_model(X_train, X_test, y_train, y_test)
