import requests
import time
import threading
import datetime


#       CHAT TELEGRAM
TOKEN_BOT = <TOKENBOT>
BASE_URL_TELEGRAM = 'https://api.telegram.org/bot'
ACCION = '/sendMessage'
ID = <ID_CHAT>


#       BINANCE
base_url = 'https://api.binance.com/api/v3'


def send_message(chat_id, msj):
    requests.post(BASE_URL_TELEGRAM + TOKEN_BOT + ACCION,
                  data={'chat_id': chat_id, 'text': msj})
    print(f'Se mando un mensaje al ID: {chat_id}')


def obtener_rsi(symbol, interval, limit):
    url = f"{base_url}/klines?symbol={symbol}&interval={interval}&limit={limit+1}"
    response = requests.get(url)
    if response.status_code == 200:
        klines = response.json()
        close_prices = [kline[4] for kline in klines]

        rsi_value = calcular_rsi(close_prices)
        print("El RSI de {} a las {} es: {}".format(interval, datetime.datetime.now().strftime('%H:%M'),rsi_value))
        return rsi_value
    else:
        print('Error al obtener los datos del RSI:', response.text)


def calcular_rsi(close_prices):
    # Calcula los cambios de precios
    price_changes = [float(close_prices[i]) - float(close_prices[i - 1]) for i in range(1, len(close_prices))]

    # Separa los cambios de precios en positivos y negativos                                                MODIFICADO
    positive_changes = [change if change > 0 else 0 for change in price_changes]
    negative_changes = [abs(change) if change < 0 else 0 for change in price_changes]

    # Calcula las medias móviles de los cambios positivos y negativos
    avg_gain = sum(positive_changes) / (len(positive_changes))
    avg_loss = sum(negative_changes) / (len(negative_changes))

    # Calcula el valor del RSI
    if avg_loss == 0:
        rsi = 100
    else:
        relative_strength = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + relative_strength))

    return round(rsi, 1)


def repetir_funcion_rsi(timer_runs, seg, period):
    while timer_runs.is_set():
        rsi = obtener_rsi('BTCUSDT', period, 14)
        if rsi < 30:
            send_message(ID, f'Posible entrada en largo!! El RSI de {period} se encuentra en {rsi}')
        elif rsi > 70:
            send_message(ID, f'Posible entrada en corto!! El RSI de {period} se encuentra en {rsi}')
        time.sleep(seg)


if __name__ == '__main__':
    timer_runs = threading.Event()
    timer_runs.set()

    a = threading.Thread(target=repetir_funcion_rsi, args=(timer_runs,300,'5m',))
    b = threading.Thread(target=repetir_funcion_rsi, args=(timer_runs, 900, '15m',))
    c = threading.Thread(target=repetir_funcion_rsi, args=(timer_runs, 3600, '1h',))
    d = threading.Thread(target=repetir_funcion_rsi, args=(timer_runs, 14400, '4h',))

    send_message(ID, 'El Bot se encuentra en Funcionamiento.')

    a.start()
    b.start()
    c.start()
    d.start()

    input('Presiona enter para detener el proceso.\n\n')

    send_message(ID, 'El Bot se encuentra en Inactivo.')

    timer_runs.clear()

    print('El proceso se ha detenido!')

