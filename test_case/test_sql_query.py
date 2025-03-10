import unittest
import logging
from sql_query import Function

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestFunction:
    def __init__(self):
        """初始化测试环境"""
        self.sql = "SELECT models FROM table WHERE name ='oneapi-token'"
        self.server = "http://IP:PORT"
        self.function = Function()

    def test_query(self):
        """测试SQL查询功能"""
        try:
            logger.info("开始测试SQL查询...")
            result = self.function.query(self.sql, self.server)
            
            if isinstance(result, dict) and 'result' in result:
                logger.info("查询成功！")
                logger.info(f"返回结果：{result}")
                return True
            else:
                logger.error("返回结果格式不正确")
                return False
                
        except Exception as e:
            logger.error(f"测试过程中发生异常: {str(e)}")
            return False

    def run_tests(self):
        """运行所有测试"""
        logger.info("开始运行测试...")
        test_results = {
            "查询测试": self.test_query()
        }
        
        # 输出测试结果摘要
        logger.info("\n测试结果摘要:")
        for test_name, result in test_results.items():
            status = "通过" if result else "失败"
            logger.info(f"{test_name}: {status}")
        
        # 返回是否所有测试都通过
        return all(test_results.values())

def main():
    """主函数"""
    test = TestFunction()
    success = test.run_tests()
    
    if success:
        logger.info("所有测试通过！")
        return 0
    else:
        logger.error("存在失败的测试！")
        return 1

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)