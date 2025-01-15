import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate

# Inicializar MetaTrader 5
if not mt5.initialize():
    print("Error al inicializar MetaTrader 5:", mt5.last_error())
    quit()

# Configurar el símbolo y la temporalidad
symbol = "EURUSDz"  # Ajusta al símbolo correcto de tu broker
timeframe = mt5.TIMEFRAME_M30  # Temporalidad de 30 minutos

# Descargar datos desde MetaTrader5
user_start_date = datetime(2024, 12, 1) # Desde el inicio del mes
adjusted_start_date = user_start_date - timedelta(days=1)
end_date = datetime.now()  # Hasta la fecha actual
rates = mt5.copy_rates_range(symbol, timeframe, adjusted_start_date, end_date)

# Verificar si se obtuvieron datos
if rates is None or len(rates) == 0:
    print("No se obtuvieron datos para el símbolo y rango especificado.")
else:
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['adjusted_date'] = df['time'].apply(
        lambda x: x.date() + timedelta(days=1) if x.hour == 23 else x.date()
    )

    # Procesar Rango 1
    def procesar_rango_1(df):
        rango_1_extremos = {}
        print("\nRango 1: Velas agrupadas de 23:00 a 07:01:")
        for current_date in sorted(df['adjusted_date'].unique()):
            start_time = datetime.combine(current_date, datetime.min.time()) - timedelta(minutes=60)
            end_time = start_time + timedelta(hours=8, minutes=1)
            rango_1_df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]

            if not rango_1_df.empty:
                max_price = rango_1_df['high'].max()
                min_price = rango_1_df['low'].min()
                rango_1_extremos[current_date] = {'max': max_price, 'min': min_price}
                print(f"\nFecha: {current_date} (desde las 23:00 hasta las 07:01)")
                print(rango_1_df[['time', 'open', 'high', 'low', 'close']])
                print(f"Máximo total: {max_price}, Mínimo total: {min_price}")

        return rango_1_extremos

    # Procesar Rango 2
    def procesar_rango_2(df, extremos_r1, tolerancia_pips=1):
        mensajes_r2 = {}
        tolerancia = tolerancia_pips / 10000
        print("\nRango 2: Velas agrupadas de 07:02 a 13:01:")
        for current_date in sorted(df['adjusted_date'].unique()):
            start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=7, minutes=2)
            end_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=13, minutes=1)
            rango_2_df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]

            if not rango_2_df.empty:
                print(f"\nFecha: {current_date} (desde las 07:02 hasta las 13:01)")
                print(rango_2_df[['time', 'open', 'high', 'low', 'close']])

                if current_date in extremos_r1:
                    max_price_r1 = extremos_r1[current_date]['max']
                    min_price_r1 = extremos_r1[current_date]['min']
                    manipulacion_detectada = None
                    for _, row in rango_2_df.iterrows():
                        high = row['high']
                        low = row['low']
                        if manipulacion_detectada is None and low < (min_price_r1 - tolerancia):
                            manipulacion_detectada = "mínimo"
                            mensaje = "Buscando compras"
                            print(f"Primera manipulación detectada: {manipulacion_detectada} ({min_price_r1}) por más de {tolerancia_pips} pips.")
                            mensajes_r2[current_date] = mensaje
                            break
                        if manipulacion_detectada is None and high > (max_price_r1 + tolerancia):
                            manipulacion_detectada = "máximo"
                            mensaje = "Buscando ventas"
                            print(f"Primera manipulación detectada: {manipulacion_detectada} ({max_price_r1}) por más de {tolerancia_pips} pips.")
                            mensajes_r2[current_date] = mensaje
                            break

        return mensajes_r2

    # Cálculo del Estocástico
    def calcular_estocastico(df, periodo_k=20, periodo_d=9, ralentizacion=9):
        """
        Calcula el Estocástico (%K y %D) con la configuración especificada.
        """
        df['Lowest Low'] = df['low'].rolling(window=periodo_k).min()
        df['Highest High'] = df['high'].rolling(window=periodo_k).max()
        df['%K'] = ((df['close'] - df['Lowest Low']) / (df['Highest High'] - df['Lowest Low'])) * 100
        df['%K'] = df['%K'].rolling(window=ralentizacion).mean()
        df['%D'] = df['%K'].rolling(window=periodo_d).mean()
        return df


def procesar_rango_3_operaciones(symbol, fondo_inicial=50000, riesgo_fijo=300, sl_pips=3.5, mensajes_r2=None):
    """
    Procesa el Rango 3 y ejecuta operaciones con un único nivel de Take Profit basado en un R:R de 1:2.
    """
    start_date_rango_3 = datetime(2024, 12, 1)  # Ajusta la fecha de inicio
    end_date_rango_3 = datetime.now()  # Ajusta la fecha de fin

    rates_m1 = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, start_date_rango_3, end_date_rango_3)
    if rates_m1 is None or len(rates_m1) == 0:
        print("No se obtuvieron datos de 1 minuto para el mes.")
        return

    df_m1 = pd.DataFrame(rates_m1)
    df_m1['time'] = pd.to_datetime(df_m1['time'], unit='s')

    # Calcular la EMA y el Estocástico
    df_m1['EMA'] = df_m1['close'].ewm(span=100, adjust=False).mean()
    df_m1['Lowest Low'] = df_m1['low'].rolling(window=20).min()
    df_m1['Highest High'] = df_m1['high'].rolling(window=20).max()
    df_m1['%K'] = ((df_m1['close'] - df_m1['Lowest Low']) / (df_m1['Highest High'] - df_m1['Lowest Low'])) * 100
    df_m1['%K'] = df_m1['%K'].rolling(window=9).mean()
    df_m1['%D'] = df_m1['%K'].rolling(window=9).mean()

    print("\nOperaciones realizadas durante el rango especificado:")
    operaciones = []
    saldo = fondo_inicial

    for current_date in sorted(df_m1['time'].dt.date.unique()):
        start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=13)
        end_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=17, minutes=31)
        rango_3_df_m1 = df_m1[(df_m1['time'] >= start_time) & (df_m1['time'] <= end_time)]

        if not rango_3_df_m1.empty:
            print(f"\nFecha: {current_date} (desde las 13:00 hasta las 17:31)")
            mensaje_rango_3 = mensajes_r2.get(current_date, "No definido")
            print(f"Mensaje del rango 3: {mensaje_rango_3}")

            for i in range(1, len(rango_3_df_m1)):
                close_anterior = rango_3_df_m1['close'].iloc[i - 1]
                ema_anterior = rango_3_df_m1['EMA'].iloc[i - 1]
                close_actual = rango_3_df_m1['close'].iloc[i]
                ema_actual = rango_3_df_m1['EMA'].iloc[i]
                k_actual = rango_3_df_m1['%K'].iloc[i]
                d_actual = rango_3_df_m1['%D'].iloc[i]

                # Determinar si la operación es compra o venta
                if mensaje_rango_3 == "Buscando compras" and close_anterior < ema_anterior and close_actual > ema_actual and k_actual < 20 and k_actual > d_actual:
                    tipo_operacion = "Compra"
                elif mensaje_rango_3 == "Buscando ventas" and close_anterior > ema_anterior and close_actual < ema_actual and k_actual > 80 and k_actual < d_actual:
                    tipo_operacion = "Venta"
                else:
                    continue

                # Calcular el tamaño de la posición
                sl = sl_pips / 10000  # SL en términos de pips convertido a decimal
                riesgo_por_lote = sl * 100000  # Riesgo por lote estándar (1.0 lote)
                tamanio_lote = riesgo_fijo / riesgo_por_lote  # Tamaño del lote necesario para arriesgar $300

                # Calcular SL y TP
                if tipo_operacion == "Compra":
                    stop_loss = close_actual - sl
                    take_profit = close_actual + (2 * sl)
                elif tipo_operacion == "Venta":
                    stop_loss = close_actual + sl
                    take_profit = close_actual - (2 * sl)

                # Simular el resultado
                resultado = 0
                for j in range(i, len(rango_3_df_m1)):
                    high = rango_3_df_m1['high'].iloc[j]
                    low = rango_3_df_m1['low'].iloc[j]

                    if tipo_operacion == "Compra":
                        if low <= stop_loss:
                            resultado = -riesgo_fijo
                            break
                        elif high >= take_profit:
                            resultado = 2 * riesgo_fijo
                            break
                    elif tipo_operacion == "Venta":
                        if high >= stop_loss:
                            resultado = -riesgo_fijo
                            break
                        elif low <= take_profit:
                            resultado = 2 * riesgo_fijo
                            break

                # Registrar operación
                operaciones.append({
                    "Fecha": rango_3_df_m1['time'].iloc[i],
                    "Tipo": tipo_operacion,
                    "Precio Entrada": close_actual,
                    "StopLoss": stop_loss,
                    "TakeProfit": take_profit,
                    "Resultado": resultado
                })

    # Mostrar resultados
    headers = ["Fecha", "Tipo", "Precio Entrada", "StopLoss", "TakeProfit", "Resultado"]
    table = [
        [op["Fecha"], op["Tipo"], op["Precio Entrada"], op["StopLoss"], op["TakeProfit"], op["Resultado"]]
        for op in operaciones
    ]
    print("\nOperaciones realizadas:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    print(f"\nSaldo final: {saldo + sum(op['Resultado'] for op in operaciones):.2f}")


extremos_r1 = procesar_rango_1(df)
mensajes_r2 = procesar_rango_2(df, extremos_r1, tolerancia_pips=1)
procesar_rango_3_operaciones(symbol, mensajes_r2=mensajes_r2)

mt5.shutdown()
