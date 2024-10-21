import datetime
import decimal
import json
import redis
# 连接Redis   158环境redis的IP地址 ----------1   5   8 ----------
# r = redis.Redis(host='10.9.7.0', port=6379, db=0, password='wazhHcz52cchC1IlUF')

# 连接Redis   230环境redis的IP地址 ----------2   3   0 ----------
r = redis.Redis(host='10.42.176.127', port=6379, db=0, password='wazhHcz52cchC1IlUF')

# 定义键为list，方便进行循环
keys = ['article_basic_data', 'article_basic_extend_data', 'article_basic_interaction_data',
        'article_basic_relation_data', 'article_basic_series_data', 'article_basic_meta_data']
# 输入文章id
article_id = "70088010"

print(f"文章ID：{article_id}")
# 打印脚本执行的当前时间
now_time = datetime.datetime.now()
print(f'查询时间：{now_time}')
if r:
    print('当前执行环境是230')
# 创建一个空字典来存储查询结果
results = {}
a = 0
for key in keys:
    # 拼接key
    ks = key + ':' + article_id
    try:
        # 查询并存储结果
        values = r.hgetall(ks)
        if not values:
            print(f"redis_key: {ks} 没有数据")
        a += 1
        # if a > 3:
        if values:  # is not None:
            cleaned_values = {
                k.decode('utf-8').replace("b'", "").replace("'", ""): v.decode('utf-8').replace("b'", "").replace(
                    "'", "") if isinstance(v, bytes) else v for k, v in values.items()}
            # 找到redis的key4，对key4的兴趣标签和标签做处理
            if a == 4:
                # print(f'value值为:{cleaned_values}')
                # 把redis的key4进行提取复制给新变量interest_tag
                if 'interest_tag' in cleaned_values and cleaned_values['interest_tag']:
                    interest_tag = cleaned_values['interest_tag']
                    json_interest_tag = json.loads(interest_tag)
                else:
                    print("======== Interest_tag数据：为空 ========")
                if 'tag' in cleaned_values and cleaned_values['tag']:
                    tag = cleaned_values['tag']
                    json_tag = json.loads(tag)
                else:
                    print("======== tag数据：为空 ========")
                # 判断interest_tag值存在
                if 'interest_tag' in cleaned_values:
                    if cleaned_values['interest_tag']:
                        cleaned_values['interest_tag'] = json_interest_tag
                    else:
                        print("interest_tag值为空，不进行转换操作")
                # 判断tag值存在
                if 'tag' in cleaned_values:
                    if cleaned_values['tag']:
                        cleaned_values['tag'] = json_tag
                    else:
                        print("tag值为空，不进行转换操作")
            # elif a > 4:
            #     print()
            results[ks] = cleaned_values
    except redis.exceptions.TimeoutError:
        print(f"redis连接超时")
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
