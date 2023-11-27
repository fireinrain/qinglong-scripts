import os

import requests


# server status 网页每月流量统计
def get_server_status_bandwidth(server_status_url: str) -> {}:
    result = {}

    url = server_status_url  # 将URL替换为实际的URL

    # 发送GET请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON响应
        json_data = response.json()

        # 初始化总和变量
        total_network_in = 0
        total_network_out = 0
        online_count = 0

        # 遍历每个服务器
        for server in json_data.get("servers", []):
            total_network_in += server.get("network_in", 0)
            total_network_out += server.get("network_out", 0)
            online_status = server.get('online4', False)
            if online_status:
                online_count += 1

        # 将总和转换为GB
        total_network_in_gb = total_network_in / (1024 ** 3)
        total_network_out_gb = total_network_out / (1024 ** 3)

        # 打印结果
        print(f"Total Network In: {total_network_in_gb:.2f} GB")
        print(f"Total Network Out: {total_network_out_gb:.2f} GB")
        result["network_in_month"] = f"{total_network_in_gb:.2f}GB"
        result["network_out_month"] = f"{total_network_out_gb:.2f}GB"
        result["network_bandwidth_total"] = f"{(total_network_in_gb + total_network_out_gb):.2f}GB"
        result["online_count"] = online_count
        from datetime import datetime

        # 获取当前年份和月份的字符串形式
        current_date = datetime.now()
        current_year_str = str(current_date.year)
        current_month_str = str(current_date.month).zfill(2)
        current_date_str = f"{current_year_str}-{current_month_str}"

        result["current_date"] = current_date_str
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    return result


def main():
    # 可以在这里设置环境遍历
    server_status_url = os.getenv("server_status_url", "<请设置为自己的server-status面板服务地址>")
    api_url = f"{server_status_url}/json/stats.json"
    status_bandwidth = get_server_status_bandwidth(api_url)
    # print(status_bandwidth)
    tgbot_message = f"""
当前年月: {status_bandwidth['current_date']}
当月累计上传流量: {status_bandwidth['network_out_month']}
当月累计下载流量: {status_bandwidth['network_in_month']}
当月总计流量: {status_bandwidth['network_bandwidth_total']}
机器在线数: {status_bandwidth['online_count']}
    """
    print(tgbot_message)
    # from notify import telegram_bot
    # telegram_bot("ServerStatus流量推送",tgbot_message)


if __name__ == '__main__':
    main()
