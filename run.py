from PySide6 import QtWidgets

from vnpy_tts.api import MdApi


class CtpMdApi(MdApi):

    def __init__(self, monitor) -> None:
        super().__init__()

        self.monitor = monitor

    def onFrontConnected(self):
        self.monitor.append("服务器连接成功")

        ctp_req = {
            "UserID": "000300",
            "Password": "vnpy1234",
            "BrokerID": "9999"
        }
        self.reqUserLogin(ctp_req, 1)

    def onFrontDisconnected(self, reason):
        self.monitor.append("服务器连接断开", reason)

    def onRspUserLogin(self, data, error, reqid, last):
        if not error["ErrorID"]:
            self.monitor.append("行情服务器登录成功")

            self.subscribeMarketData("rb2301")
        else:
            self.monitor.append("行情服务器登录失败", error)

    def onRtnDepthMarketData(self, data):
        self.monitor.append(str(data))


def main():
    app = QtWidgets.QApplication()

    monitor = QtWidgets.QTextEdit()
    monitor.show()

    api = CtpMdApi(monitor)
    api.createFtdcMdApi(".")
    # api.registerFront("tcp://180.168.146.187:10130")  # ctp
    api.registerFront("tcp://122.51.136.165:20004")
    api.init()

    app.exec()


if __name__ == "__main__":
    main()
