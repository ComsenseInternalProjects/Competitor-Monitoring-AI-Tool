import http.client
import json


# Function to fetch data from the API
def fetch_data_from_api(botid, taskid):
    conn = http.client.HTTPSConnection("api.browse.ai")
    headers = {
        'Authorization': "Bearer ************************************************"
    }
    url = f"/v2/robots/{botid}/tasks/{taskid}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

# Function to fetch Google news data from the API
def fetch_google_data_from_api(botid, taskid):
    conn = http.client.HTTPSConnection("api.browse.ai")
    headers = {
        'Authorization': "Bearer *****************************************************"
    }
    url = f"/v2/robots/{botid}/tasks/{taskid}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)



