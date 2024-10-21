import requests
import json

# 设置API的URL
URL = "https://article-api.smzdm.com/zhiyoushuo/shaiwu/biji_list"
# 设置请求头
headers = {"Host": "article-api.smzdm.com",
           "user-agent": "smzdm_android_V11.0.20.67 rv:1030 (22041211AC;Android13;zh)smzdmapp",
           "request_key": "809152491719452570",
           "content-type": "application/x-www-form-urlencoded"}
# token={"token":"BB-1FtnGaFW09vG8RZQef9JtpqtzhSRbpIcyoW6tADwt0GvU8o%2F3AcCeD%2BqGea9PV0xryI8F7AYEKzdb9HYL612tF9msQ4%3D"}
cookie = {
    "z_me": "",
    "partner_name": "smzdm_catch",
    "sess": "BB-1FtnGaFW09vG8RdDo3VwWuHiwRLPnJalBrikr%2F143dQI9wD1V3XFht9za5bJIRdq5WWZk7vs1cT5JXkoWsrGHpGtHXA%3D;",
    "pid": "device_type=Redmi22041211AC;z_dr=6c947c2e9a771eaec81405450cff0c6b",
    "sessionID": "b0d807ef45c5a6090f3876c4a0d5172a.1719452503585",
    "basic_v": "0",
    "login": "1",
    "client_id": "b0d807ef45c5a6090f3876c4a0d5172a.1719381069974",
    "register_time": "1703219407",
    "network": "1",
    "device_system_version": "13",
    "partner_id": "9998",
    "device_s": "6c947c2e9a771eaec81405450cff0c6b",
    "smzdm_version": "11.0.20.67",
    "ab_test": "x",
    "device_smzdm": "android",
    "apk_partner_name": "smzdm_catch",
    "smzdm_id": "7960592775",
    "device_id": "6c947c2e9a771eaec81405450cff0c6b",
    "device_push": "1",
    "apk_partner_id": "9998",
    "session_id": "b0d807ef45c5a6090f3876c4a0d5172a.1719391643218",
    "device_smzdm_version": "11.0.20.67",
    "device_rid": "b0d807ef45c5a6090f3876c4a0d5172a",
    "active_time": "1716356691",
    "z_ai": "b9714e0784826a22e2ffc4100452c65b",
    "new_device_id": "6c947c2e9a771eaec81405450cff0c6b",
    "is_new_user": "0",
    "last_article_info": "",
    "device_recfeed_setting": "%7B%22haojia_recfeed_switch%22%3A%220%22%2C%22homepage_sort_switch%22%3A%221%22%2C%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D",
    "device_smzdm_version_code": "1030"
}
# 设置请求参数
data = {
    "zhuanzai_ab": "b",
    "weixin": "1",
    "offset": "0",
    "f": "android",
    "v": "11.0.20.67",
    "order_field": "",
    "sign": "CB37EEA2FEEEFE3B947C50F5A3F79FC2",
    "status_str": "",
    "time": "1719453329000",
    "basic_v": "0",
    "token": "BB-1FtnGaFW09vG8RdDo3VwWuHiwRLPnJalBrikr%2F143dQI9wD1V3XFht9za5bJIRdq5WWZk7vs1cT5JXkoWsrGHpGtHXA%3D"}

# 发送请求
response = requests.post(URL, headers=headers, data=data, cookies=cookie)
print(response.text)
# 解析响应数据
data = json.loads(response.text)
print(data)
# 提取所有的article_id
ids = []
for dict_item in data['data']:
    row = dict_item['rows']
    for item in row:
        article_id = item['article_id']
        ids.append(article_id)
print(ids)
