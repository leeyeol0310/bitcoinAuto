# 슬렉 연동 코드
import time
import pyupbit
import datetime
import requests

access = ""
secret = ""
myToken = ""

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    # df.iloc[0]['close'] 다음날 시가와 동일
    # (df.iloc[0]['high'] - df.iloc[0]['low']) * k : 변동폭
    # target_price : 목표값
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP") # 09:00
        end_time = start_time + datetime.timedelta(days=1) # 09:00 + 1일

        # 09:00 < 현재 < 08:59:50 현재 시간이 이조건을 만족하면
        if start_time < now < end_time - datetime.timedelta(seconds=10): # 시작시간괴 끝나는시간
            target_price = get_target_price("KRW-XRP", 0.1) # get_target_price(변동성전략 매수가)를 내가 원하는데로 구현해서 0.5 = K값을 조정해서 할수도있다
            """변동성 돌파 전략으로 매수 목표가 조회"""

            ma5 = get_ma5("KRW-XRP") # 현재 가격이
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma5 < current_price:
                # target_price : 목표각겨보다
                # current_price : 현재가격이 높다면

                krw = get_balance("KRW") # 그떄 KRW 내 원화 잔고를 조회하고
                if krw > 5000: # 이게 최소 거래 금액이 5천원 이상이면
                    buy_result = upbit.buy_market_order("KRW-XRP", krw*0.9995) # 코인을 매수
                    post_message(myToken,"#stock", "XRP buy : " +str(buy_result))
        else: # 09:00 < 현재 < 08:59:50 -> 8시59분50초 에서 9시 전일때
            XRP = get_balance("XRP") # 당일 종가에 코인을 전량 매도 하는 코드
            if XRP > 0.00008: # 현재 가지고있는 금액이 5천원 이상이면 전량 매도 하는 코드
                sell_result = upbit.sell_market_order("KRW-XRP", XRP*0.9995)
                post_message(myToken,"#stock", "XRP buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)

  
  
