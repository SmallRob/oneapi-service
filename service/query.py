from flask import Flask, request, jsonify, Blueprint
from sqlalchemy import create_engine, text
import os
import sys

bp = Blueprint('query', __name__, url_prefix='/oneapi')

# 从环境变量获取数据库配置
DB_HOST = os.environ.get('DB_HOST', 'mysql')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_USER = os.environ.get('DB_USER', 'oneapi')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '123456')
DB_NAME = os.environ.get('DB_NAME', 'one-api')

# 配置数据库连接
DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

try:
    # 尝试导入 pymysql
    import pymysql
    # 创建数据库引擎
    engine = create_engine(DATABASE_URI)
    # 测试连接
    with engine.connect() as conn:
        pass
    print(f"数据库连接成功: {DB_HOST}:{DB_PORT}/{DB_NAME}")
except ImportError:
    print("错误: 缺少 PyMySQL 包。请使用 'pip install pymysql' 安装。", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"数据库连接错误: {str(e)}", file=sys.stderr)
    # 在开发环境中，我们仍然允许应用程序启动，便于调试
    if not os.environ.get('FLASK_ENV') == 'development':
        # 在生产环境中，如果数据库连接失败，应该停止应用程序
        sys.exit(1)

@bp.route('/query', methods=['POST'])
def query_database():
    # 获取请求中的SQL语句
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "无效的请求数据",
            "data": None
        }), 400
    
    sql_query = data.get('sql')
    if not sql_query:
        return jsonify({
            "success": False,
            "message": "SQL查询语句是必须的",
            "data": None
        }), 400
    
    try:
        # 执行SQL查询
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
            # 将结果转换为字典列表
            columns = result.keys()
            result_list = [dict(zip(columns, row)) for row in rows]
            
            return jsonify({
                "success": True,
                "message": "查询成功",
                "data": result_list
            })
    except Exception as e:
        print(f"查询执行错误: {e}", file=sys.stderr)
        return jsonify({
            "success": False,
            "message": f"查询错误: {str(e)}",
            "data": None
        }), 500