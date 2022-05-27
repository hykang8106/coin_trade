import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from upbit.client import Upbit
# import pykorbit

from doge_trade import access_key, secret_key

market = "KRW-ETH"
 
form_class = uic.loadUiType("window.ui")[0]
 
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.inquiry)
 
    def inquiry(self):
        """ price = pykorbit.get_current_price("BTC")
        print(price) """

        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)

        # 클라이언트 객체 생성
        client = Upbit(access_key, secret_key)

        # get current price
        # 요청 당시 종목의 스냅샷을 반환합니다.
        resp = client.Trade.Trade_ticker(
            markets=market
        )
        # print_json(resp['result'])
        price = resp['result'][0]['trade_price']
        # print(price)
        self.lineEdit.setText(str(price))

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()