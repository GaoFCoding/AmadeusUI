import socket as sc
from socket import socket

"""
    build socket between UI(clienter) and v2 (server)
"""

class SocketClient(socket):
    def __init__(self, host:str ="127.0.0.1", port:int = 5000) -> None:
        self.host = host
        self.port = port
        self.Client_Pool = [] #socket连接池

    def SocketServerKeeper(self):
        if len(self.Client_Pool) < 1:
            print("open server ... ")
            s = socket(sc.AF_INET, sc.SOCK_STREAM) #创建socket连接对象
            s.bind((self.host,self.port))
            s.listen(1) #socket允许的最大连接数为1（单线程）

            print("正在等待连接的建立...")
            client, _ = s.accept()
            self.Client_Pool.append(client) #将连接加入到连接池中
            print("已与客户端建立连接，通信开始")
        else:
            print("连接数为:{},请先处理当前连接对象".format(len(self.Client_Pool)))

    def SendData(self,data)->str:
        try:
            self.Client_Pool[0].send(data.encode())
            return "ok"
        except:
            self.Client_Pool[0].close() #关闭当前连接
            del self.Client_Pool[0] #移出连接池
            return -1
        ...

    def RecData(self)->str:
        try:
            res = self.Client_Pool[0].recv(1024).decode() #最多每次接受1024个字节
            if len(res) > 0:
                return res
            else:
                return -1
        except:
            self.Client_Pool[0].close() #关闭当前连接
            del self.Client_Pool[0] #移出连接池
            return -1
        ...

    def RemoveFromPool(self):
        del self.Client_Pool[0]
        ...