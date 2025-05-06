from common import *

# Clash Verge API 配置
api_url = "http://127.0.0.1:9097/proxies/Proxy"  # 替换为你的分组名称
nodes = [
    "T1-台湾01",
    "T1-新加坡1",
    "T1-日本01",
    "T1-美国01",
    "T1-韩国01",
    "T1-香港01",
]  # 替换为你的节点名称列表
interval = 1800  # 切换间隔（秒）


def switch_proxy(node):
    headers = {"Content-Type": "application/json"}
    payload = {"name": node}
    try:
        response = requests.put(api_url, json=payload, headers=headers)
        if response.status_code == 204:
            print(f"Switched to node: {node}")
            # 检查当前 IP（可选）
            ip_response = requests.get("https://api.ipify.org?format=json")
            current_ip = ip_response.json()["ip"]
            print(f"Current IP: {current_ip}")
        else:
            print(f"Failed to switch to {node}: {response.text}")
    except Exception as e:
        print(f"Error switching to {node}: {e}")

