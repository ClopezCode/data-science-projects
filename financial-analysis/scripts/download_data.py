import os
import yfinance as yf

def download_stock_data(ticker, start_date, end_date, output_file):
    """
    Descarga datos históricos de una acción y los guarda en un archivo CSV.
    """
    # Crear la carpeta si no existe
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Descargar datos con yfinance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Convertir el índice de fechas a una columna normal
    data.reset_index(inplace=True)

    # Guardar datos en un CSV sin duplicar índices
    data.to_csv(output_file, index=False)  # index=False elimina el índice adicional
    print(f"Datos de {ticker} guardados en {output_file}")

if __name__ == "__main__":
    ticker = "AAPL"  # Cambia esto al ticker deseado
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    output_file = "financial-analysis/data/AAPL.csv"

    download_stock_data(ticker, start_date, end_date, output_file)
