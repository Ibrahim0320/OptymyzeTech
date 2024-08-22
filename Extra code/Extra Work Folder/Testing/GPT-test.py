# Testing different stuff on the gpt API
import requests
import json

url = "https://api.openai.com/v1/completions"

payload = json.dumps({
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Translate the following sentence into French: 'My name is Ben'"
    }
  ]
})
headers = {
  'Cookie': '_cfuvid=7FWlKxWBzVV8ukB8LTNt25PKGtMRIUUTR3bzaBd30PU-1715171900178-0.0.1.1-604800000; __cf_bm=hH4B_Dk6qGKXCytrSu3p4XbHpCPjOuIUJyjyx1J3vuQ-1715173799-1.0.1.1-QIsSXcnWfPCNKLCwnkFOLH8QXEPHXaEPIBXNSR29regrwseJM38GQ1zqCc9k8aTe2ay.q0l_eyKx9AMyfUE6yQ',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
