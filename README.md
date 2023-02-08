# AmaduesUI
>Amadeus version2.0

## 技术栈
1. RenPy
2. Python
3. ChatGPT
4. VOSK
5. TTS

## 介绍

### 项目内容
该项目实现了对**Amadeus**的简单复刻，能够实现与ChatGPT饰演的Amadeus助手进行**即时对话**，支持线上模式和离线模式，线上模式需要启动本地socket服务器（v2.py文件），通过socket连接RenPy客户端与本地服务端；在交互上支持**文本输入**与**语音输入**两种模式，推荐使用语音输入，带来的沉浸感更强

***
### 如何使用
1. 项目未对python环境打包，需要你自己配置好程序运行所需要的环境，最好使用anaconda创建虚拟环境方便包管理，程序运行所需的依赖我已经在`requirements.txt`中列出

环境配置流程：

服务端环境配置：
1. 首先创建好新的虚拟环境后（假设你创建的环境名为`demo`）

2. 用conda命令切换`conda activate demo`

3. 然后`cd`到该项目的目录下，`pip install -r requirements`安装所有依赖


客户端打包：
1. 你需要安装renpy，并将程序打包，生成Amadeus.exe可执行文件
2. RenPy项目界面点击`操作`->`构建发行版`进行程序打包

**最后，在一切准备就绪后，运行v2.py文件，可以在vscode等编辑器中运行或者通过命令行`python v2.py`运行，在输出等待客户端连接后，执行`amadeus.exe`可执行文件，即可开始游戏**

***
### 注意
1. 本程序通过直接获取本地的sqlit数据库文件获取openai的登录token令牌，因此必须要求你使用chrome浏览器，若要改成手动输入token，请自行修改代码
2. 由于openai服务器是国外的，且不支持中国及中国香港地区的使用，因此需要使用代理，建议梯子挂在日本
3. 在使用前，你必须注册自己的openai账号，请自行上网查找注册指南
4. 仓库未使用lfs存储，因此并未上传运行所需的VOSK，TTS模型文件，需要模型的朋友可以通过下面链接自取：
vosk-model-cn-0.15
https://www.aliyundrive.com/s/ykW5XHJEwa8
提取码: 89cd

G265000.pth
链接：https://pan.baidu.com/s/1IqbQp-wnJQSiyB-irRHTIQ 
提取码：gaof

将`vosk-model-cn-0.15`文件夹放入到voice2Text目录，将`G265000.pth`放入到TTS_model目录下即可

5. 语音识别需要将`ffmpeg.exe`和`ffprobe.exe`两个文件放到项目目录下，可以自行去官网下载获取，或者通过下面的链接自取：
https://www.aliyundrive.com/s/BiB2yxoJhJF
提取码: 6m9i

也可以尝试使用自己训练的模型来进行替换，这里就不讲述教程了，自行阅读代码，非常的简单（需要替换模型与模型相关配置的json文件）
