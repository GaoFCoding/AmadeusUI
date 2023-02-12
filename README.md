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
1. 本程序通过直接获取本地的sqlit数据库文件获取openai的登录token令牌，因此必须使用chrome浏览器，若要改成手动输入token，请自行修改代码
2. 访问openai服务器需要使用代理，建议梯子挂在日本，不过好像香港地区已经可以访问了？
3. 在使用前，你必须注册自己的openai账号，请自行上网查找注册指南
4. 可以自行将服务端改为可实现远程部署的版本，但是不推荐，因为目前使用的该wrapper还不太稳定，需要本地监控调试，等后续openai真正开放chatgpt的api的时候会进行相应的修改
5. UI窗口输出的中文是将chatgpt的日文回复通过调用百度翻译API实现的，要使用此功能需要自行前往http://api.fanyi.baidu.com 获取自己的api key，并在chatgpt/translate.py中修改,或者更换其他API（百度翻译要钱，免费的每月限制5w字符）
6. 仓库未使用lfs存储，因此并未上传运行所需的VOSK，TTS模型文件，需要模型的朋友可以通过下面链接自取，或者使用自己的模型替换：
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
6. 初始化ChatGPT设定的文件在`./chatgpt/init_chatgpt.txt`，可以自行根据喜好修改chatGPT扮演设定。

### 更新计划
1. 目前还是demo版本，完全是出于个人兴趣制作的一个简易版本，本人大三了准备考研，后续如果不太忙会继续更新的
2. 目前使用的vosk模型是官方开源的，可直接在官网下载，VITS模型暂时使用的是huggingface上大佬开源的模型，本人还在不断调参训练中，后续若效果可以的话会替换成自己训练的模型
3. 后续优先计划是把模型训练好，可以考虑在这基础上再添加比屋真帆定的角色设定及TTS模型。其次就是对交互界面进行优化，目前的界面设计比较简陋，后续考虑使用live2d实现可动立绘等，或者在这基础上嵌入更多的除了调用chatgpt之外的一些功能（甚至计算机视觉？哈哈哈，再说吧）
4. 语言模型在不断迭代，之后还会有GPT4等，等openai真正开放chatgpt的接口，或者是有更高级的语音模型的时候我会跟进的
