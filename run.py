from PySide6 import QtWidgets, QtCore

from vnpy_tts.api import MdApi


class SimpleWidget(QtWidgets.QWidget):

    signal = QtCore.Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.api = None

        self.log_monitor = QtWidgets.QTextEdit()
        self.log_monitor.setReadOnly(True)

        self.subscribe_button = QtWidgets.QPushButton("订阅")
        self.symbol_line = QtWidgets.QLineEdit()

        self.subscribe_button.clicked.connect(self.subscribe_symbol)
        self.signal.connect(self.log_monitor.append)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.log_monitor)
        vbox.addWidget(self.symbol_line)
        vbox.addWidget(self.subscribe_button)

        self.setLayout(vbox)

    def subscribe_symbol(self):
        symbol = self.symbol_line.text()
        self.api.subscribeMarketData(symbol)


class CtpMdApi(MdApi):

    def __init__(self, widget) -> None:
        super().__init__()

        self.widget = widget

    def onFrontConnected(self):
        self.monitor.append("服务器连接成功")
        self.widget.signal.emit("服务器连接成功")

        ctp_req = {
            "UserID": "000300",
            "Password": "vnpy1234",
            "BrokerID": "9999"
        }
        self.reqUserLogin(ctp_req, 1)

    def onFrontDisconnected(self, reason):
        self.widget.signal.emit("服务器连接断开", reason)

    def onRspUserLogin(self, data, error, reqid, last):
        if not error["ErrorID"]:
            self.widget.signal.emit("行情服务器登录成功")
        else:
            self.widget.signal.emit("行情服务器登录失败", error)

    def onRtnDepthMarketData(self, data):
        self.widget.signal.emit(str(data))


def main():
    app = QtWidgets.QApplication()

    widget = SimpleWidget()
    widget.show()

    api = CtpMdApi(widget)
    widget.api = api

    api.createFtdcMdApi(".")
    # api.registerFront("tcp://180.168.146.187:10130")  # ctp
    api.registerFront("tcp://122.51.136.165:20004")
    api.init()

    app.exec()


if __name__ == "__main__":
    main()
