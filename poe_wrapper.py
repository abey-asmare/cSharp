from poe_api_wrapper import PoeApi
bot = 'a2'
TOKEN = '4Ti_eGta1vh34hC5FcJbtg%3D%3D'
client = PoeApi(TOKEN)
# response = client.send_message(bot, '52-40=__?? 12, -9, 9, 32')

message = "hey poe for the question i'll be asking you from now on you will give me only the answer accurately without description. I'll provide you two types of question, the first one is some kind of ordering and i wanted the answer ordered not with comma but with newline character separated and dont use some type of description like 1. 2. 3. 4. or a. b. c. d. the other one is simple just answering what i asked you, and i wanted only one anwer without description"
new_message = 'what direction did i give you?'
response = client.send_message(bot, new_message, chatCode='2k3ne6hz6b7z6bud69j')
print(response['response'])
