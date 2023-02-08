import socket
import time
"""
    build socket between UI(clienter) and v2 (server)
"""

host = "127.0.0.1"
port = 5000
Client_Pool = [] #全局socket连接池

# print("open server ... ")
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #创建socket连接对象
# s.bind((host,port))
# print("waiting for client in 20 second")
# s.listen(1) #socket允许的最大连接数 

# print("正在等待连接的建立...")
# client, client_addr = s.accept()
# print("已与客户端建立连接，通信开始")


def SocketServerKeeper():
    global Client_Pool
    print("open server ... ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #创建socket连接对象
    s.bind((host,port))
    s.listen(1) #socket允许的最大连接数 

    print("正在等待连接的建立...")
    client, _ = s.accept()
    Client_Pool.append(client) #将连接加入到连接池中
    print("已与客户端建立连接，通信开始")

def SendData(data)->str:
    global Client_Pool
    try:
        Client_Pool[0].send(data.encode())
        return "ok"
    except:
        Client_Pool[0].close() #关闭当前连接
        del Client_Pool[0] #移出连接池
        return -1
    ...

def RecData()->str:
    global Client_Pool
    try:
        res = Client_Pool[0].recv(1024).decode() #最多每次接受1024个字节
        if len(res) > 0:
            return res
        else:
            return -1
    except:
        Client_Pool[0].close() #关闭当前连接
        del Client_Pool[0] #移出连接池
        return -1
    ...

def RemoveFromPool():
    global Client_Pool
    del Client_Pool[0]
    ...