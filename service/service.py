from flask import Flask
from get_models import bp as get_data

app = Flask(__name__)

# 统一注册路由
app.register_blueprint(get_data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5800)
