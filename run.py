# from vnpy_ctp.api import MdApi
from vnpy_tts.api import MdApi


class CtpMdApi(MdApi):

    def __init__(self) -> None:
        super().__init__()

    def onFrontConnected(self):
        print("服务器连接成功")


if __name__ == "__main__":
    api = CtpMdApi()
    api.createFtdcMdApi(".")
    # api.registerFront("tcp://180.168.146.187:10130")  # ctp
    api.registerFront("tcp://122.51.136.165:20004")
    api.init()
    input()
