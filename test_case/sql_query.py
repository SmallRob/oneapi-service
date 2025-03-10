import urllib3
import json
import logging
from urllib3.exceptions import HTTPError
from typing import TypedDict, List, Optional

class ModelData(TypedDict):
    models: str

class QueryResponse(TypedDict):
    data: List[ModelData]
    message: str
    success: bool

def validate_response(response_data: dict) -> bool:
    """验证响应数据的格式是否正确"""
    required_fields = {'data', 'message', 'success'}
    return all(field in response_data for field in required_fields)

# 设置更详细的日志格式
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main(sql: str, serv: str) -> dict:
    try:
        logger.debug(f"开始查询，SQL: {sql}")
        logger.debug(f"服务器地址: {serv}")

        data = {"sql": sql}
        url = f'{serv}/query'
        
        # 配置连接池管理器，添加重试机制
        retries = urllib3.Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        http = urllib3.PoolManager(
            retries=retries,
            timeout=urllib3.Timeout(connect=5.0, read=10.0)
        )

        json_data = json.dumps(data).encode('utf-8')
        logger.debug(f"发送请求到: {url}")
        logger.debug(f"请求数据: {json_data}")

        # 发送请求并获取详细的错误信息
        try:
            response = http.request(
                method='POST',
                url=url,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body=json_data
            )
        except HTTPError as he:
            logger.error(f"HTTP请求错误: {he}")
            return {"result": f"HTTP请求错误: {he}"}

        logger.debug(f"响应状态码: {response.status}")
        logger.debug(f"响应头: {response.headers}")
        logger.debug(f"响应体: {response.data}")

        if response.status != 200:
            error_msg = f"请求失败，状态码: {response.status}"
            try:
                error_data = json.loads(response.data.decode('utf-8'))
                error_msg += f", 错误详情: {error_data}"
            except json.JSONDecodeError:
                error_msg += f", 响应内容: {response.data.decode('utf-8', errors='ignore')}"
            raise Exception(error_msg)

        response_data = response.data.decode('utf-8')
        parsed_result = json.loads(response_data)
        logger.info(f"查询成功，返回数据: {parsed_result}")

        # 验证响应格式
        if not validate_response(parsed_result):
            raise ValueError("响应数据格式不正确")
            
        if not parsed_result['success']:
            raise Exception(f"查询失败: {parsed_result['message']}")
            
        # 类型转换
        typed_response: QueryResponse = parsed_result
        
        logger.info(f"查询成功，返回数据: {typed_response}")
        
        return {
            "result": typed_response
        }

    except json.JSONDecodeError as je:
        error_msg = f"JSON解析错误: {je}"
        logger.error(error_msg)
        return {"result": error_msg, "success": False}
    except ValueError as ve:
        error_msg = f"数据验证错误: {ve}"
        logger.error(error_msg)
        return {"result": error_msg, "success": False}
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return {"result": str(e), "success": False}