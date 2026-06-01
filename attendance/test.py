import xml.etree.ElementTree as ET
import requests


class SMSService:
    def __init__(self, base_url='http://192.168.8.1'):
        self.base_url = base_url

    def _get_tokens(self):
        """Fetches session and verification tokens from HiLink API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/webserver/token", timeout=5
            )
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                token_el = root.find('token')
                token = token_el.text if token_el is not None else None
                return token
        except (requests.RequestException, ET.ParseError) as e:
            print(f"Error fetching modem token: {e}")
        return None

    def send_sms(self, phone, message):
        """Sends an SMS payload via HTTP POST to the modem."""
        token = self._get_tokens()
        if not token:
            print("Failed to authenticate with modem. SMS not sent.")
            return False

        url = f"{self.base_url}/api/sms/send-sms"
        
        payload = f"""<?xml version='1.0' encoding='UTF-8'?>
        <request>
            <Index>-1</Index>
            <Phones><Phone>{phone}</Phone></Phones>
            <Sca></Sca>
            <Content>{message}</Content>
            <Length>{len(message)}</Length>
            <Reserved>1</Reserved>
            <Date>-1</Date>
        </request>"""

        headers = {
            "__RequestverificationToken": token,
            "content-Type": "application/xml",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            res = requests.post(url, data=payload, headers=headers, timeout=5)
            if "OK" in res.text:
                print(f"🎉 Success! SMS transmitted to {phone}")
                return True
            print(f"❌ Modem rejected message. Response: {res.text}")
        except requests.RequestException as e:
            print(f"❌ Failed to transmit SMS: {e}")
        return False

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Initialize the service
    gateway = SMSService()
    
    # ⚠️ CHANGE THESE TO YOUR TEST VALUES
    TARGET_PHONE = "0900011***"  # Use your actual phone number format here
    TEST_MESSAGE = "Hello! This is a live test from the Django School SMS System."

    print("Initiating connection to Huawei E3372...")
    gateway.send_sms(TARGET_PHONE, TEST_MESSAGE)
