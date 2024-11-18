import requests
import frappe
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """
    创建带有重试机制的会话。
    """
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session

def call_etsy_api(endpoint, method="GET", headers=None, data=None, params=None):
    """
    通用的 Etsy API 调用方法。

    :param endpoint: API 端点路径，例如 'orders/{order_id}'
    :param method: HTTP 方法（GET, POST, PUT, DELETE）
    :param headers: 请求头
    :param data: POST 或 PUT 请求的数据
    :param params: URL 参数
    :return: JSON 响应
    """
    base_url = "https://openapi.etsy.com/v3/application"
    url = f"{base_url}/{endpoint}"

    session = create_session()

    try:
        response = session.request(method, url, headers=headers, json=data, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        frappe.log_error(f"Etsy API Error: {e} | Endpoint: {endpoint}")
        raise

def validate_etsy_credentials(api_key, access_token):
    """
    验证 Etsy API 凭据。

    :param api_key: API Key
    :param access_token: 访问令牌
    :return: 布尔值，表示凭据是否有效
    """
    headers = {
        "x-api-key": api_key,
        "Authorization": f"Bearer {access_token}",
    }
    try:
        call_etsy_api("openapi-ping", headers=headers)
        return True
    except Exception:
        return False

def refresh_etsy_token(client_id, client_secret, refresh_token):
    """
    刷新 Etsy API 的访问令牌。

    :param client_id: Etsy 应用的 Client ID
    :param client_secret: Etsy 应用的 Client Secret
    :param refresh_token: 用户的刷新令牌
    :return: 包含新令牌信息的 JSON 数据
    """
    url = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    session = create_session()

    try:
        response = session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        frappe.log_error(f"Failed to refresh Etsy token: {e}")
        raise

def fetch_etsy_order_details(api_key, access_token, order_id):
    """
    获取 Etsy 订单的详细信息。

    :param api_key: API Key
    :param access_token: 访问令牌
    :param order_id: Etsy 订单 ID
    :return: 订单详情 JSON 数据
    """
    headers = {
        "x-api-key": api_key,
        "Authorization": f"Bearer {access_token}",
    }
    return call_etsy_api(f"orders/{order_id}", headers=headers)

def log_etsy_error(context, error_message):
    """
    记录 Etsy 相关的错误日志。

    :param context: 错误发生的上下文信息
    :param error_message: 错误消息
    """
    frappe.log_error(f"[Etsy] Context: {context} | Error: {error_message}")
