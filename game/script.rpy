# 初始化相关参数与python脚本
define a = Character("Amadeus红莉栖")
define u = Character("冈部(You)")
define s = Character("Amadeus System")
define bgm = "music/bgm.mp3"
image amadeus = "images/per.png"
image background = "gui/background.png"
image downline_bg = "gui/downline_bg.png"
define config.gl2 = True
image kuris = Live2D("resources/amadeus/per_speak.model3.json", base=1.0, loop = True, fade=False)



# 游戏在此开始。
label start:
    with dissolve
    scene background
    play music bgm

    menu optional_name:
        s "请选择交互模式"
        "在线模式":
            jump ConnectServer
        "离线模式":
            jump DownLine
            
label DownLine:
    show kuris speaking
    # show amadeus
    voice "/audio/downline.ogg"
    voice sustain
    a "不好意思，这个功能还没做出来噢"
    return


label ConnectServer:
    python:
        isConn = True
        try:
            import socket
            waiting = 0
            total_data = bytes()
            host = "127.0.0.1"
            port = 5000
            renpy.block_rollback() #回滚阻塞，防止回滚到当前语句之前的脚本

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            client.connect((host,port)) #socket客户端连接服务端
        except:
            isConn = False

    if isConn == False:
        jump ConnectWrong

    $ renpy.block_rollback() #止回滚到当前语句之前的脚本。

    jump WaitingForServer


label ConnectWrong:
    with dissolve
    s "与服务器握手失败，请检查服务器是否正常运作"
    return

#等待服务端初始化完成
label WaitingForServer:
    $ renpy.block_rollback()
    s "已与服务端建立握手，等待服务端程序初始化..."        
    jump Waiting

label Waiting:
    s "..."
    python:
        client.setblocking(0) #设置非阻塞
        try:
            data = client.recv(1024).decode() #阻塞，直到服务端初始化完成
        except:
            data = bytes()

    if len(data) > 0 and data == "first":
        s "服务端初始化已完成，进入模式选择阶段..."
        jump choiceYourInput
    
    if len(data) > 0 and data == "second":
        s "正在恢复上一次会话..."
        jump choiceYourInput

    jump Waiting


#选择输入方式
label choiceYourInput:
    $ renpy.block_rollback()#回滚阻塞，防止回滚到当前语句之前的脚本
    menu inputMethod:
        s "请选择你与Amadeus的交互方式..."
        "keyboard":
            python:
                client.send(("0").encode())
                keyboard = True
            jump talk_keyboard
        "voice":
            python:
                client.send(("1").encode())
                keyboard = False
            jump waitingForModel


label talk_keyboard:
    show kuris breathing
    $ renpy.block_rollback()
    python:
        message = renpy.input("冈部(You)：")
        client.send(message.encode())
        data = bytes()
    jump checkRes

label waitingForModel:
    show kuris breathing
    s "等待声学模型加载..."
    python:
        client.setblocking(1) #设置阻塞
        isModelOK = client.recv(1024) #在此等待，直到模型加载完成
    if isModelOK.decode() == "ok":
        u "正在输入语音..."
        jump talk_voice
    jump waitingForModel

label talk_voice:
    $ renpy.block_rollback()
    
    python:
        client.setblocking(0) #非阻塞
        try:
            finishInput = client.recv(1024)
        except: #非阻塞时若获取不到会直接返回错误，因此进行错误捕捉
            finishInput = bytes()
            # client.setblocking(1)

    if(len(finishInput) > 0):
        $ finishInput = finishInput.decode()
        $ renpy.block_rollback() #防止回滚
        u "[finishInput]"
        jump checkRes
    jump talk_voice
    
label checkRes:
    $ renpy.block_rollback()
    a "..."

    python:
        client.setblocking(0)
        try:
                data = client.recv(1024)
                total_data += data
        except:
                data = bytes()
                # client.setblocking(1)
    if(len(data) > 0 and len(data) < 1024): #获取到回复
        python:
            response = total_data.decode()
            total_data = bytes()

        if response == "quit":
            $ client.close() #断开连接
            show kuris speaking
            voice "/audio/saybye.ogg"
            a "那么，下次再见，冈部"
            voice sustain
            with dissolve
            return

        if response == "retry":
            s "请尝试重新输入..."
            if keyboard:
                jump talk_keyboard
            else:
                jump waitingForModel
        
        jump answer

    else:
        $ renpy.block_rollback()
        a "..."
        jump checkRes
            

label answer:
    show kuris speaking
    voice "/audio/output.ogg"
    $ renpy.block_rollback()
    a "[response]"
    voice sustain
    
    if keyboard:
        $ client.send("语音播放完毕".encode())
        jump talk_keyboard
    else:
        $ client.send("语音播放完毕".encode())
        jump waitingForModel