import datetime
import decimal
import json
import redis


# 连接Redis
r = redis.Redis(host='10.9.7.0', port=6379, db=0, password='wazhHcz52cchC1IlUF')
# 定义包含六个键的列表
keys = ['article_basic_data', 'article_basic_extend_data', 'article_basic_interaction_data',
        'article_basic_relation_data', 'article_basic_series_data', 'article_basic_meta_data']
# 输入文章id
# article_id = input("输入文章id:")
article_id = "70247940"  # 输入文章id-------------
# 创建一个空字典来存储查询结果
results = {}
a = 0
for key in keys:
    # 拼接key
    ks = key + ':' + article_id
    try:
        # 查询并存储结果
        values = r.hgetall(ks)
        a += 1
        # if a > 3:
        if values:  # 这里直接判断是否为空，为空则不进行后续处理
            cleaned_values = {
                k.decode('utf-8').replace("b'", "").replace("'", ""): v.decode('utf-8').replace("b'", "").replace(
                    "'", "") if isinstance(v, bytes) else v for k, v in values.items()}
            if a == 4:
                print(f'value值为:{cleaned_values}，看到报错不要慌。。。只是redis没数据而已。。。。')
                interest_tag = cleaned_values['interest_tag']
                json_interest_tag = json.loads(interest_tag)
                tag = cleaned_values['tag']
                json_tag = json.loads(tag)
                cleaned_values['interest_tag'] = json_interest_tag
                cleaned_values['tag'] = json_tag
            # elif a > 4:
            #     print()
            results[ks] = cleaned_values
        # print(type(results))
    except redis.exceptions.TimeoutError:
        print(f"redis 超时")


class Encode(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)


try:
    results_json = json.dumps(results, indent=None, cls=Encode)
    # 打印结果
    print(results_json)
except TypeError as e:
    print(f"转换为JSON时出错: {e}")
