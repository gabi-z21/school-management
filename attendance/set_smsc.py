import requests
import xml.etree.ElementTree as ET

BASE_URL = 'http://192.168.8.1'

def force_smsc():
    # 1. Fetch the security token
    try:
        token_res = requests.get(f"{BASE_URL}/api/webserver/token", timeout=5)
        root = ET.fromstring(token_res.text)
        token = root.find('token').text
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        return

    # 2. CHOOSE YOUR CARRIER GATEWAY NUMBER HERE
    # Ethio Telecom: "+251911299708" or "+251911000014"
    # Safaricom: "+251700000010"
    SMSC_NUMBER = "+251911000014" 

    payload = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<request>"
        f"<Sca>{SMSC_NUMBER}</Sca>"
        "</request>"
    )

    headers = {
        "__RequestVerificationToken": token,
        "Content-Type": "application/xml",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # Pushing the gateway number directly to the cellular card
        endpoint = f"{BASE_URL}/api/sms/save-sms-sc"
        res = requests.post(endpoint, data=payload, headers=headers, timeout=5)
        if "OK" in res.text or res.status_code == 200:
            print(f"🎉 Success! SMS Center number forced to: {SMSC_NUMBER}")
            print("The modem now knows where to route outgoing texts.")
        else:
            print(f"❌ Modem rejected the config. Response: {res.text}")
    except Exception as e:
        print(f"❌ Transmission error: {e}")

if __name__ == "__main__":
    force_smsc()