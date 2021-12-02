from logging import currentframe
import websocket, json
import dateutil.parser

minutes_processed = {}
minute_candlesticks = []
current_tick = None
previous_tick = None

def on_open(ws):
    print("opened connection")

    subscribe_message = {
        "type":"subscribe",
        "channels":[
            {
                "name":"ticker",
                "product_ids": [
                    "DOGE-USD"
                ]
            }
        ]
    }

    ws.send(json.dumps(subscribe_message))

def on_message(ws,message):
    global current_tick, previous_tick

    previous_tick = current_tick
    current_tick = json.loads(message)
    print("=== Received Tick ===")
    print("{} @ {}".format(current_tick['time'],current_tick['price']))

    tick_datetime_object = dateutil.parser.parse(current_tick['time'])
    tick_dt = tick_datetime_object.strftime("%m/%d/%Y %H:%M")
    print(tick_datetime_object.minute)
    print(tick_dt)

    if not tick_dt in minutes_processed:
        print("starting new candlestick")
        minutes_processed[tick_dt] = True
        print(minutes_processed)

        if len(minute_candlesticks) > 0:
            minute_candlesticks[-1]['close'] = previous_tick['price']
        minute_candlesticks.append({
            "minute":tick_dt,
            "open":current_tick['price'],
            "high":current_tick['price'],
            "low":current_tick['price']
        })

    if len(minute_candlesticks) > 0:
        current_candlestick = minute_candlesticks[-1]
        if current_tick['price'] > current_candlestick['high']:
            current_candlestick['high'] = current_tick['price']
        if current_tick['price'] < current_candlestick['low']:
            current_candlestick['low'] = current_tick['price']

        print("== Candlesticks ==")
        for candlestick in minute_candlesticks:
            print(candlestick)

socket = "wss:
