import datetime
import decimal
import json
import pymysql
article_id = 70088010  # 输入文章 id-------------
# 数据库连接配置
try:
    # 158环境mysql_ip地址  10.10.158.170
    # 230环境mysql_ip地址  10.10.182.129
    connection = pymysql.connect(
        # host='10.10.158.170',   # 158环境mysql的IP地址
        host='10.10.182.129',  # 230环境mysql的IP地址
        user='article_user',
        password='ywewwruigyu5',
        database='smzdm_article',
    )
    # 尝试建立与数据库的连接，并打印连接信息（如果成功建立连接）
    # print(f"打印数据库连接信息：{connection.get_server_info()}")
    with connection.cursor() as cursor:
        # 需要执行的SQL
        sqls = {
            "SQL_1": f"""SELECT ab.title,ab.title_series_title,ab.image,ab.comment_switch,SUBSTRING(ab.content2, 1, 200) AS content2,
ai.article_hash_id,ai.user_id,ai.anonymous,ai.channel_id,ai.article_status,ai.is_delete,ai.publishtime,ai.reproduce_id #,ai.article_id
FROM article_index AS ai LEFT JOIN article_base AS ab
ON ai.article_id = ab.article_id
WHERE ai.article_id = {article_id} GROUP BY ai.article_id;""",
            # 查询文章的标题、系列标题、图片、评论开关、部分内容、文章哈希 ID、用户 ID、是否匿名、频道 ID、文章状态、是否删除、发布时间等信息
            "SQL_2": f"""SELECT ai.project_id,ab.start_effective_time,ab.end_effective_time,ab.first_publish,adf.gc,adf.dp_from
FROM article_index AS ai LEFT JOIN article_base AS ab
ON ai.article_id = ab.article_id
LEFT JOIN article_auditflow AS adf
ON ai.article_id = adf.article_id
WHERE ai.article_id = {article_id} GROUP by ai.article_id;""",
            # 查询文章的项目 ID、开始生效时间、结束生效时间、首次发布时间、审核流中的一些字段
            "SQL_3": f"""SELECT ais.comment_count,ais.collection_count,ais.collection_count_rl,ais.up_count,ais.up_count_rl,ais.up_count_recommender,ais.shang_action_count,ais.shang_person_count, aix.hot_count
FROM article_index AS aix
LEFT JOIN article_interaction AS ais
ON aix.article_id = ais.article_id
WHERE aix.article_id = {article_id}  GROUP BY aix.article_id;""",
            # 查询文章的评论数、热度
            "SQL_4_brand_id_品牌id": f"""SELECT brand_id FROM article_brand WHERE article_id = {article_id};""",
            # 查询文章的品牌 ID
            "SQL_4_mall_id_商城id": f"""SELECT mall_id FROM article_mall WHERE article_id = {article_id};""",
            # 查询文章的商城 ID
            "SQL_4_category_id_分类id": f"""SELECT category_id FROM article_main_category WHERE article_id = {article_id};""",
            # 查询文章的主分类 ID
            "SQL_4_article_main_category_relation_分类子集id": f"""SELECT level_first,level_second,level_third,level_four FROM article_main_category_relation WHERE article_id = {article_id};""",
            # 查询文章在子分类 ID
            "SQL_4_article_tag_标签id": f"""SELECT tag_id,source_from,type,special_type,is_delete FROM article_tag WHERE article_id = {article_id}  and is_delete = 0;""",
            # 查询文章的标签 ID、来源、类型、
            "SQL_4_Interest_tag_兴趣标签": f"""SELECT tag_id,score,tag_path,status,source_from,sub_source_from,editor_id,editor_name FROM article_interest_tag WHERE article_id = {article_id} AND status = 1 ;""",
            # 查询文章的兴趣标签相关信息，当状态为 1 时
            "SQL_5_series_id&series_order_id": f"""SELECT ai.series_id AS index_series_id,amt.meta_key,amt.meta_value
FROM article_index AS ai JOIN article_meta AS amt
ON ai.article_id = amt.article_id 
WHERE amt.meta_key LIKE "series_order_id" AND  ai.article_id = {article_id}   GROUP BY ai.article_id;""",
            # 查询文章的系列 ID 和元数据中的系列 ID 相关信息
            "SQL_6_meta表数据": f"""SELECT  meta_key,meta_value FROM article_meta
WHERE meta_key IN ('shaiwu_video_type', 'square_pic_url', 'video_type', 'is_video', 'video_id', 'video_duration')  
AND article_id =  {article_id} ;"""
            # 查询文章元数据中特定的视频相关信息
        }
        results = {}
        for key, sql in sqls.items():
            cursor.execute(sql)
            # 执行每条 SQL 语句
            rows = cursor.fetchall()
            # 获取查询结果
            if rows:
                columns = [desc[0] for desc in cursor.description]
                # 获取查询结果的列名
                result_list = []
                for row in rows:
                    result_dict = {}
                    for index, value in enumerate(row):
                        result_dict[columns[index]] = value
                        # 将每一行的结果与列名对应起来，存储在字典中
                    result_list.append(result_dict)
                results[key] = result_list
        #         将结果存储在 results 字典中，以 SQL 语句的键为索引
finally:
    print(f"文章ID：{article_id}")
    try:
        connection.close()
        print("======== 连接关闭 ========")
        # 关闭数据库连接，释放资源
    except NameError:
        pass
# 将结果转换为 JSON
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
# 定义一个 JSON 编码器类，用于处理特定类型的数据转换为 JSON 格式
data_dict = {}
for key, value in results.items():
    if value:
        # 直接将value（假设它是一个可迭代对象）赋给字典的对应键
        data_dict[key] = list(value) if hasattr(value, '__iter__') and not isinstance(value, str) else [value]
# 将 results 中的结果整理到 data_dict 字典中
data = json.dumps(data_dict, indent=None, cls=Encode, separators=(',', ':'))
# 将 data_dict 转换为 JSON 字符串，使用自定义的编码器类 Encode，并指定分隔符
# 打印执行的时间
now_time = datetime.datetime.now()
print(f'查询时间：{now_time}')
print(data)
