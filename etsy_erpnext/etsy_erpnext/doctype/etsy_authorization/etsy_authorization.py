# etsy_erpnext/doctype/etsy_authorization/etsy_authorization.py

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from etsy_erpnext.utils.etsy_utils import validate_etsy_credentials, refresh_etsy_token

class EtsyAuthorization(Document):
    """
    管理Etsy授权信息的文档类。
    """

    def before_save(self):
        """
        在保存文档之前验证API凭据并处理令牌。
        """
        # 检查必要字段是否存在
        required_fields = ["api_key", "api_secret", "access_token", "refresh_token"]
        for field in required_fields:
            if not getattr(self, field, None):
                frappe.throw(f"{field.replace('_', ' ').title()} is required.")
        
        # 验证API凭据
        if not validate_etsy_credentials(
            api_key=self.api_key,
            access_token=self.access_token
        ):
            frappe.throw("Invalid Etsy API credentials. Please verify and try again.")
        
        # 检查令牌是否即将过期
        if self.token_expiry and datetime.strptime(self.token_expiry, "%Y-%m-%d %H:%M:%S") <= datetime.now():
            self.refresh_access_token()

    def refresh_access_token(self):
        """
        刷新访问令牌。
        """
        try:
            # 调用工具函数刷新令牌
            new_token_data = refresh_etsy_token(
                api_key=self.api_key,
                api_secret=self.api_secret,
                refresh_token=self.refresh_token
            )
            # 更新令牌数据
            self.access_token = new_token_data.get("access_token")
            self.token_expiry = (datetime.now() + timedelta(seconds=new_token_data.get("expires_in", 3600))).strftime("%Y-%m-%d %H:%M:%S")
            frappe.msgprint("Access token successfully refreshed.")
        except Exception as e:
            frappe.log_error(f"Failed to refresh access token for Etsy Authorization {self.name}: {e}")
            frappe.throw("Failed to refresh access token. Please check the logs for more details.")

    def on_trash(self):
        """
        在删除文档时执行的操作。
        """
        frappe.msgprint(f"Etsy Authorization '{self.name}' has been removed.")
