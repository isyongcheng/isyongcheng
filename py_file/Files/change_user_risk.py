import pymysql
user_risk_db_config = {
    'host': '10.42.85.127',
    'user': 'cc_res_user',
    'password': 'bG6Y2WgPSVvJ1bNG',
    'database': 'commercial_res',
}
# 创建连接
connection = pymysql.connect(**user_risk_db_config)
# 创建游标
user_id = "11303604"  # 输入用户id
is_risk = 0
try:
    with connection.cursor() as cursor:
        sql_select = f""" SELECT * FROM `talent_user_risk` WHERE user_id = {user_id} """
        cursor.execute(sql_select)
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            columns_list = []
            for row in rows:
                datadict = {}
                for index, value in enumerate(row):
                    datadict[columns[index]] = value
                columns_list.append(datadict)
            print(columns_list)
            sql_update = f""" UPDATE talent_user_risk SET is_risk = {is_risk} WHERE user_id = {user_id} """
            # sql执行
            cursor.execute(sql_update)
            # 更新数据
            connection.commit()
            print(f"用户：{user_id}风险等级修改成功，风险字段：{is_risk}， 【0:否，1:是】")
        else:
            print(f"用户：{user_id}不存在")
except Exception as e:
    print(f"修改失败：{str(e)}")
finally:
    connection.close()
