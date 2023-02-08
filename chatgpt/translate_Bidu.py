import random
import hashlib
import http
import json
import urllib

appid = '20230204001549890'  # 填写你的appid
secretKey = 'IqMxbyJ_Z35uddDeeEld'  # 填写你的密钥

def baiduTranslate(translate_text):
    """
        translate API from BaiDu
    """

    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址
    fromLang = 'auto'  # 原文语种

    toLang = 'zh'  # 译文语种

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
    finally:
        if httpClient:
            httpClient.close() #关闭连接


# if __name__ == '__main__':
#     # 手动录入翻译内容，q存放
#     # q = raw_input("please input the word you want to translate:")
#     q = "こんにちは"
#     '''
#     flag=1 输入的句子翻译成英文
#     flag=0 输入的句子翻译成中文
#     '''
#     result = baiduTranslate(q)  # 百度翻译
#     print("原句:"+q)
#     print(result)