import http.client
import json
import os
import time
import base64

# Function Entry Point
def airlines_spec(url_airlines : str, captcha_rule_id : str, target_site:str, site_key:str):
    conn = http.client.HTTPSConnection("h96x7mlmud.execute-api.ap-southeast-1.amazonaws.com")

    # get token from windows environment variable
    myToken = os.environ.get('captcha-breaker-token')

    # call API submitCaptchaRequest
    conn.request("POST", "/production/submitCaptchaRequest",
                 airlines_spec_str(url_airlines, captcha_rule_id, target_site, site_key),
                 authorization_headers(myToken))

    res = conn.getresponse()
    data = res.read()

    data_json: dict = json.loads(data)
    id_string = data_json.get('data', {}).get('id', '')
    print(f'id string 1 : {id_string}')
    payload = json.dumps({
        'id': id_string,
    })

    time.sleep(2)

    status = 'QUEUED'
    loop_counter = 0
    loop_max = 15
    delay_second = 2

    # loop at 15 times and stop if status not success
    while status != 'SUCCESS':
        if loop_counter > loop_max:
            break

        # call API getResponseCaptcha
        conn.request("POST", "/production/getResponseCaptcha", payload, authorization_headers(myToken))
        res = conn.getresponse()
        data = res.read()
        data_json: dict = json.loads(data)
        status = data_json.get('data', {}).get('status', '')
        print(f'STATUS={status} loop_counter={loop_counter}')
        loop_counter += 1
        time.sleep(delay_second)

    # write file to get captcha response
    with open("outputGetCaptcha.json", "wt") as fileOutput:
        fileOutput.write(data.decode("utf-8"))

    # get string response
    data_json: dict = json.loads(data)
    str_response = data_json.get('data', {}).get('response', '')
    print(f'id string 1 : {str_response}')
    payload = json.dumps({
        'response': str_response,
    })

    return str(f'{status}')


def authorization_headers(token: str):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }


def airlines_spec_str(_url_airlines, _captcha_rule_id, _target_site, _site_key):
    if f'{_site_key}' == "":
        
        #convert image on local server to base64 for image captcha
        with open("captchaImage.png", "rb") as img_base64:
            str_img = base64.b64encode(img_base64.read()).decode('utf-8')

        return json.dumps({
                "captchaRuleId": f'{_captcha_rule_id}',
                "config": {
                    "retry": 10,
                    "timeout": 50000,
                    "timeDelayAfterSubmitted": 10000,
                    "delayPolling": 5000
                },
                "captchaSpec": {
                    "fileType": "IMAGE",
                    "body": f'{str_img}',
                    "pageUrl": f'{_url_airlines}'
                },
                "targetSite": f'{_target_site}',
                "targetSiteType": "flight",
                "domain": "eci"
            })

    return json.dumps({
        "captchaRuleId": f'{_captcha_rule_id}',
        "config": {
            "retry": 10,
            "timeout": 50000,
            "timeDelayAfterSubmitted": 10000,
            "delayPolling": 5000
        },
        "captchaSpec": {
            "fileType": "TEXT",
            "body": f'{_site_key}',
            "pageUrl": f'{_url_airlines}'
        },
        "targetSite": f'{_target_site}',
        "targetSiteType": "flight",
        "domain": "eci"
    })
