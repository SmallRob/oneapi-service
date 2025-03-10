
import csv
import json
def main(csv_string):
    # 将CSV字符串分割成行
    lines = csv_string.strip().split('\n')
    # 使用csv模块读取数据
    reader = csv.reader(lines)
    # 将所有行转换为列表
    data = [row for row in reader]
    # 检查数据是否为空
    if not data or len(data) < 2:
        return {"output": "Error: CSV data is empty or invalid."}
    # 将数字字符串转换为浮点数
    for row in data[1:]:  # 跳过标题行
        for i in range(1, len(row)):
            try:
                row[i] = float(row[i])
            except ValueError:
                row[i] = None  # 如果转换失败，设置为 None
    # 创建完整的ECharts配置
    echarts_config = {
        "title": {
            "text": "数据可视化"
        },
        "legend": {
            "data": data[0][1:]  # 使用标题行作为图例
        },
        "tooltip": {},
        "dataset": {
            "source": data
        },
        "xAxis": [
            {"type": "category", "gridIndex": 0},
            {"type": "category", "gridIndex": 1}
        ],
        "yAxis": [
            {"gridIndex": 0},
            {"gridIndex": 1}
        ],
        "grid": [
            {"bottom": "55%"},
            {"top": "55%"}
        ],
        "series": [
            # 根据数据列数动态生成系列
            {"type": "bar", "seriesLayoutBy": "row"} for _ in range(len(data[0]) - 1)
        ] + [
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1} for _ in range(len(data[0]) - 1)
        ]
    }
    # 生成输出文件
    output = "```echarts\n" + json.dumps(echarts_config, indent=2, ensure_ascii=False) + "\n```"
    return {"output": output}