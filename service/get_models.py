import os
from flask import Flask, jsonify,Blueprint
import mysql.connector

bp = Blueprint('get_models', __name__, url_prefix='/oneapi/')


# 从环境变量获取数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD','password'),
    'database': os.getenv('DB_NAME', 'oneapi'),
    'port': os.getenv('DB_PORT', '3306')
}

token_name = os.getenv('TOKEN_NAME', 'oneapi-token')

def query_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT models FROM tokens WHERE name = %s", (token_name,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@bp.route('get_models', methods=['GET'])
def get_data():
    data = query_data()
    return jsonify({'data': data})
    #return jsonify({'data': 'hello world'})
