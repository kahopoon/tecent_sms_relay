# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from flask import Flask, redirect, url_for, request, json

app = Flask(__name__)

@app.route('/sendSms', methods = ['POST'])
def send_sms():
  api_key = request.headers.get('API-KEY')
  api_secret = request.headers.get('API-SECRET')
  app_id = request.headers.get('APP-ID')
  sms_template_id = request.headers.get('SMS-TEMPLATE-ID')
  body_params = str(request.get_data().decode('utf-8')).split("&")
  body_params_dict = {}
  for x in body_params:
    key_value = x.split("=")
    body_params_dict[key_value[0]] = key_value[1]
  print(body_params_dict)
  phone_number = body_params_dict['number']
  sms_message = body_params_dict['message']
  request_remarks = body_params_dict['remarks']
  try:
    cred = credential.Credential(api_key, api_secret)
    httpProfile = HttpProfile()
    httpProfile.reqMethod = "POST"
    httpProfile.reqTimeout = 30
    httpProfile.endpoint = "sms.na-toronto.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.signMethod = "TC3-HMAC-SHA256"
    clientProfile.language = "en-US"
    clientProfile.httpProfile = httpProfile
    client = sms_client.SmsClient(cred, "ap-singapore", clientProfile)
    req = models.SendSmsRequest()
    req.SmsSdkAppId = app_id
    req.ExtendCode = ""
    req.SessionContext = request_remarks
    req.SenderId = ""
    req.PhoneNumberSet = [phone_number]
    req.TemplateId = sms_template_id
    req.TemplateParamSet = [sms_message]
    resp = client.SendSms(req)
    response = app.response_class(
        response=json.dumps({'success': True, 'message': json.loads(resp.to_json_string())}),
        status=200,
        mimetype='application/json'
    )
    return response
  except TencentCloudSDKException as err:
    response = app.response_class(
      response=json.dumps({'success': False, 'message': err}),
      status=200,
      mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
