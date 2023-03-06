import openai

"""
    the following function uses chatgpt api with the model which calls
    'gpt-3.5-turbo'.
"""

TalkingNoteBook = [] #communication history record

openai.api_key = "填写你自己的chatgpt—api"

def InitChatGPT():
    with open("./chatgpt/init_chatgpt.txt",encoding='utf-8') as textfile:
        initChatgptText =  textfile.read()
    
    TalkingNoteBook.append({"role":"system","content":initChatgptText})
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=TalkingNoteBook
    )

    response = res['choices'][0]['message']['content']
    TalkingNoteBook.append({"role":"assistant","content":response}) #add to history record

def SendRequest(reqMsg:str):
    """
        send request to openai server and receive the response
    """
    if "再见" in reqMsg:
        return "quit"
    
    TalkingNoteBook.append({"role":"user","content":reqMsg})
    res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=TalkingNoteBook
        )
    
    response = res['choices'][0]['message']['content']
    TalkingNoteBook.append({"role":"assistant","content":response}) #add to history record
    return response



