import pandas as pd
import matplotlib.pyplot as plt

def plot_moving_averages(file_path, window1=50, window2=200):
    """
    Grafica el precio de cierre y las medias móviles.
    """
    # Leer el archivo CSV
    data = pd.read_csv(file_path, parse_dates=["Date"])
    data.set_index("Date", inplace=True)  # Usar "Date" como índice

    # Convertir a numérico para evitar errores
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data.dropna(subset=['Close'], inplace=True)  # Eliminar filas con valores NaN

    # Calcular medias móviles
    data['SMA_50'] = data['Close'].rolling(window=window1).mean()
    data['SMA_200'] = data['Close'].rolling(window=window2).mean()

    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Precio de cierre', alpha=0.75)
    plt.plot(data['SMA_50'], label=f'Media móvil {window1} días', linestyle='--')
    plt.plot(data['SMA_200'], label=f'Media móvil {window2} días', linestyle='--')
    plt.title('Precio de cierre y medias móviles')
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    file_path = "financial-analysis/data/AAPL.csv"
    plot_moving_averages(file_path)
