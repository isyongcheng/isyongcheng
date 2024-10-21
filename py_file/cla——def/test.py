import base64
import json
import redis
# 连接Redis
r = redis.Redis(host='10.9.7.0', port=6379, db=0, password='wazhHcz52cchC1IlUF')
# 定义包含六个键的列表
keys = ['article_basic_data', 'article_basic_extend_data', 'article_basic_interaction_data',
        'article_basic_relation_data', 'article_basic_series_data', 'article_basic_meta_data']
# 输入文章id
id = input("输入文章id:")
# 创建一个空字典来存储查询结果
results = {}
for key in keys:
    # 拼接key
    ks = key + ":" + id
    # 查询并存储结果
    values = r.hgetall(ks)
    # 修改---
    if values:
        results[ks]=values
    # print(values)
    # results[ks] = values
# 打印结果
print("查询结果：", results)
# 转换为JSON格式
# results_json = json.dumps(results)
# print('转换为JSON格式的结果:',results_json)
# # 转换为Base64编码
# results_base64 = base64.b64encode(results_json.encode('utf-8'))
# # 打印Base64编码后的结果
# print("Base64编码后的结果：", results_base64.decode('utf-8'))