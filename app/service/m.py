import requests
import json
  
# defining the api-endpoint 
API_ENDPOINT = "https://ieepo075.webhook.office.com/webhookb2/c7ea4d84-d6ef-4cf6-bd3f-49f0ff75c239@7f26df61-0a0f-433a-9e40-55818dac1c9b/IncomingWebhook/84a3b1831d454d7ca14f032c68c9e4dd/c16251dd-f713-4ae0-afcb-17b16fd7b4ef"
#API_ENDPOINT="https://web.hook.sh/ba9755da-d652-47b3-a8d7-145b0dfdacf5"
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


data={"type":"MessageCard",
    "title": "Publish Adaptive Card Schema",
     "text":"Testing webhook2",
    "description": "Now that we have defined the main rules and features of the format, we need to produce a schema and publish it to GitHub. The schema will be the starting point of our reference documentation.",
    "creator": {
        "name": "Matt Hidinger",
        "profileImage": "https://pbs.twimg.com/profile_images/3647943215/d7f12830b3c17a5a9e4afcc370e3a37e_400x400.jpeg"
    },
    "createdUtc": "2017-02-14T06:08:39Z",
    "viewUrl": "https://adaptivecards.io",
    "properties": [
        { "key": "Board", "value": "Adaptive Cards" },
        { "key": "List", "value": "Backlog" },
        { "key": "Assigned to", "value": "Matt Hidinger" },
        { "key": "Due date", "value": "Not set" }
    ]
}

data={ "$schema": "http://adaptivecards.io/schemas/adaptive-card.json", "type": "AdaptiveCard", "version": "1.0", "body": [ { "type": "Container", "items": [ { "type": "TextBlock", "text": "Publish Adaptive Card with emojis 🥰 ", "weight": "bolder", "size": "medium" }, ] }, ], }
data={
    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "summary":" resumen",
    "text":"<p>parrafo</p><h2>header</h2><p><br></br>",
    "version": "1.0",
    "body": [
        {
            "type": "TextBlock",
            "text": "This is some **bold** text"
        },
        {
            "type": "TextBlock",
            "text": "This is some _italic_ text"
        },
        {
            "type": "TextBlock",
            "text": "- Bullet \r- List \r",
            "wrap": "true"
        },
        {
            "type": "TextBlock",
            "text": "1. Numbered\r2. List\r",
            "wrap": "true"
        },
        {
            "type": "TextBlock",
            "text": "Check out [Adaptive Cards](https://adaptivecards.io)"
        }
    ]
}
print (data)
app_json = json.dumps(data)
print(app_json)

# data to be sent to api
  
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = app_json)
  
# extracting response text 
pastebin_url = r.text
print("Return is:%s"%pastebin_url)