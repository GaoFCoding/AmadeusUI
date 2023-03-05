import random
import hashlib
import http
import json
import urllib
from googletrans import Translator 

#百度api
appid = '20230204001549890'  # 填写你的appid
secretKey = 'aWc8Iq9dG4CaRdQb0IFP'  # 填写你的密钥

def TranslateByBaidu(translate_text, toLang:str = "zh", fromLang:str = "auto"):
    """
        translate API from BaiDu
    """
    
    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

    salt = random.randint(3276, 65536)

    sign = appid + translate_text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # return result
        return result['trans_result'][0]['dst']

    except Exception as e:
        print(e)
        return translate_text #翻译失败返回原文
    finally:
        if httpClient:
            httpClient.close() #关闭连接

#谷歌翻译api
def TranslateByGoogle(translate_text):
    try:
        translator = Translator(service_urls=[
            'translate.google.cn',
            'translate.google.com',
            ])

        trans=translator.translate(translate_text, src='ja', dest='zh-cn')
    except Exception as e:
        print(e)
        return translate_text #翻译失败返回原文
    return trans.text #返回译文

