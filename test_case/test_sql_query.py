from sql_query import main

# 测试参数
test_sql = "SELECT models FROM table WHERE name ='oneapi-token'"
test_server = "http://IP:PORT"

try:
    # 调用主函数
    result = main(test_sql, test_server)
    print("查询成功！")
    print("返回结果：", result)
except Exception as e:
    print("发生错误：", str(e))