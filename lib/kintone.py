import ssl
import adafruit_requests
import json
import socketpool
import wifi
import gc

def uploadRecord(subDomain, apiToken, record):
    url = "https://" + subDomain + ".kintone.com/k/v1/record.json"
    headers = {"X-Cybozu-API-Token": apiToken,
               "Content-Type": "application/json"}

    try:
        if wifi.radio.connected:
            pool = socketpool.SocketPool(wifi.radio)
        else:
            print("No Wi-Fi connection!")
            return 1

        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        response = requests.post(url, headers=headers, json=record)

        if response.status_code == 200 and "id" in json.loads(response.text):
            print("Record uploaded.", end=" ")
            recordId = json.loads(response.text)["id"]
            print("Record ID: " + recordId)

            return recordId
        else:
            print("Record upload failed. Status code: " + str(response.status_code))
            return None
        
    except Exception as e:
        print("Error:", e)
        return None

    finally:
        if response:
            try:
                response.close()
            except Exception as e:
                print("Error closing response:", e)
                
        requests = None
        gc.collect()
