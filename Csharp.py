from poe_api_wrapper import PoeApi

TOKEN = '4Ti_eGta1vh34hC5FcJbtg%3D%3D'
client = PoeApi(TOKEN)

def chat(message:str, chatId:int = 290769770)-> str:
         for chunk in client.send_message('aviscsharphelper', message=message, chatId=chatId):
            if chunk['state'] == 'complete':
                return chunk['text']


chat('hello how are you');