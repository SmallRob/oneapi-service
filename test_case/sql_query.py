import urllib3
import json
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(sql: str, serv: str) -> dict:
    try:
        logger.debug(f"开始查询，SQL: {sql}")
        logger.debug(f"服务器地址: {serv}")

        data = {"sql": sql}
        # 不要覆盖 serv 参数
        url = f'{serv}/query'
        # 创建连接池管理器
        http = urllib3.PoolManager()

        # 编码请求数据
        json_data = json.dumps(data).encode('utf-8')
        print(json_data)

        logger.debug(f"发送请求到: {url}")
        logger.debug(f"请求数据: {json_data}")

        # 发送 POST 请求
        response = http.request(
            method='POST',
            url=url,
            headers={'Content-Type': 'application/json'},
            body=json_data
        )

        logger.debug(f"响应状态码: {response.status}")

        # 检查响应状态（可选，但推荐）
        if response.status != 200:
            raise Exception(f"请求失败，状态码: {response.status}")

        # 解析响应数据
        response_data = response.data.decode('utf-8')
        parsed_result = json.loads(response_data)
        print(parsed_result)

        return {
            "result": parsed_result
        }

    except Exception as e:
        logger.error(f"查询失败: {e}")
        return {
            "result": f"查询失败: {e}"
        }