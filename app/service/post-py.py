import requests
import json
  
# defining the api-endpoint 
API_ENDPOINT = "https://ieepo075.webhook.office.com/webhookb2/c7ea4d84-d6ef-4cf6-bd3f-49f0ff75c239@7f26df61-0a0f-433a-9e40-55818dac1c9b/IncomingWebhook/84a3b1831d454d7ca14f032c68c9e4dd/c16251dd-f713-4ae0-afcb-17b16fd7b4ef"
#API_ENDPOINT="https://web.hook.sh/2492acf4-3823-4956-8179-aedb20511cc2"  
# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here
source_code = '''
print("Hello, world!")
a = 1
b = 2
print(a + b)
'''
data=    {
        
        
        "title": "Backup generado",
        "subtitle": "10-Febrero-2022",
        "text": "Se ha generado el archivo : IEEPO-TEST-20220209.bak",  
        "summary":"Testing webhook",
        "images": 
                    {
                        "url": "https://icon-library.com/images/back-up-icon/back-up-icon-10.jpg",
                        "alt": "backup"
                    }
                ,
        }


data={
   "type":"Post",
   "attachments":[
      {
         "contentType":"application/vnd.microsoft.card.adaptive",
         "contentUrl":"",
         "content":{
            "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
            "type":"AdaptiveCard",
            "version":"1.2",
            "body":[
                {
                "type": "TextBlock",
                "text": "For Samples and Templates, see [https://adaptivecards.io/samples](https://adaptivecards.io/samples)"
                }
            ]
         }
      }
   ]
}

app_json = json.dumps(data)
print(app_json)

# data to be sent to api
  
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = app_json)
  
# extracting response text 
pastebin_url = r.text
print("Return is:%s"%pastebin_url)