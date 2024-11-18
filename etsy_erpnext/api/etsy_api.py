import frappe
from etsy_erpnext.utils.etsy_utils import (
    validate_etsy_credentials,
    refresh_etsy_token,
    fetch_etsy_order_details,
    log_etsy_error,
    call_etsy_api,
)

def get_authorization_details():
    """
    获取最新的 Etsy 授权信息。
    
    :return: 包含 API Key、Access Token、Client ID、Client Secret、Refresh Token 的字典
    """
    authorization = frappe.get_all("Etsy Authorization", filters={"enabled": 1}, limit_page_length=1)
    if not authorization:
        frappe.throw("No active Etsy Authorization found.")
    
    auth_doc = frappe.get_doc("Etsy Authorization", authorization[0].name)
    return {
        "api_key": auth_doc.api_key,
        "access_token": auth_doc.access_token,
        "client_id": auth_doc.client_id,
        "client_secret": auth_doc.client_secret,
        "refresh_token": auth_doc.refresh_token,
    }

def synchronize_etsy_orders():
    """
    同步 Etsy 订单到 ERPNext。
    每小时执行一次。
    """
    try:
        # 获取授权信息
        auth_details = get_authorization_details()
        api_key = auth_details["api_key"]
        access_token = auth_details["access_token"]

        # 检查凭据有效性
        if not validate_etsy_credentials(api_key, access_token):
            frappe.log_error("Etsy credentials invalid. Attempting to refresh token.")
            # 刷新令牌
            refreshed_token = refresh_etsy_token(
                client_id=auth_details["client_id"],
                client_secret=auth_details["client_secret"],
                refresh_token=auth_details["refresh_token"],
            )
            # 更新数据库中的访问令牌
            update_authorization_token(refreshed_token["access_token"])
            access_token = refreshed_token["access_token"]

        # 调用 Etsy API 获取订单
        endpoint = "shops/YOUR_SHOP_ID/receipts"  # 替换为您的商店 ID
        params = {"limit": 100}  # 可根据需要修改
        headers = {
            "x-api-key": api_key,
            "Authorization": f"Bearer {access_token}",
        }
        response = call_etsy_api(endpoint, method="GET", headers=headers, params=params)

        # 处理订单数据
        for order in response.get("results", []):
            create_or_update_order_in_erpnext(order)

    except Exception as e:
        log_etsy_error("Synchronize Etsy Orders", str(e))
        frappe.log_error(f"Etsy Order Sync Failed: {e}")

def create_or_update_order_in_erpnext(order_data):
    """
    在 ERPNext 中创建或更新 Etsy 订单。

    :param order_data: 单个 Etsy 订单的 JSON 数据
    """
    try:
        order_id = order_data.get("receipt_id")
        existing_order = frappe.db.exists("Etsy Order", {"etsy_order_id": order_id})

        if existing_order:
            order_doc = frappe.get_doc("Etsy Order", existing_order)
        else:
            order_doc = frappe.new_doc("Etsy Order")
            order_doc.etsy_order_id = order_id

        # 更新订单字段
        order_doc.customer_name = order_data.get("name")
        order_doc.total_amount = order_data.get("grandtotal")
        order_doc.currency = order_data.get("currency_code")
        order_doc.order_date = order_data.get("creation_tsz")
        order_doc.status = order_data.get("status")
        order_doc.save()
        frappe.db.commit()

    except Exception as e:
        log_etsy_error("Create or Update Order in ERPNext", str(e))
        frappe.log_error(f"Failed to create or update order: {e}")

def update_authorization_token(new_access_token):
    """
    更新数据库中的 Access Token。

    :param new_access_token: 新的 Access Token
    """
    try:
        authorization = frappe.get_all("Etsy Authorization", filters={"enabled": 1}, limit_page_length=1)
        if not authorization:
            frappe.throw("No active Etsy Authorization found.")

        auth_doc = frappe.get_doc("Etsy Authorization", authorization[0].name)
        auth_doc.access_token = new_access_token
        auth_doc.save()
        frappe.db.commit()

    except Exception as e:
        log_etsy_error("Update Authorization Token", str(e))
        frappe.log_error(f"Failed to update Etsy Authorization token: {e}")
