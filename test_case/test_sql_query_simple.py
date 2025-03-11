import logging
from sql_query import query

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 修改SQL查询语句，使用正确的表名格式
test_sql = "SELECT models FROM `aise-oneapi`.tokens WHERE name = 'oneapi-token'"
test_server = "https://xxx/oneapi"

try:
    # 调用查询函数
    result = query(test_sql, test_server)
    
    print("查询成功！")
    print("返回结果：", result)
    
    # 检查返回结果,如果是json对象
    # if isinstance(result, str):
    #     try:
    #         parsed_result = json.loads(result)
    #         print("查询成功！")
    #         print("返回结果：", parsed_result)
    #     except json.JSONDecodeError:
    #         print("查询失败！")
    #         print("错误信息：", result)
        
except Exception as e:
    print("发生异常：", str(e))