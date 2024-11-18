# etsy_erpnext/doctype/etsy_order/etsy_order.py

import frappe
from frappe.model.document import Document
from etsy_erpnext.utils.etsy_utils import fetch_etsy_order_details

class EtsyOrder(Document):
    """
    管理Etsy订单数据的文档类。
    """

    def before_save(self):
        """
        在保存文档之前处理订单状态和验证数据。
        """
        if not self.etsy_order_id:
            frappe.throw("Etsy Order ID is required.")
        
        # 检查是否需要更新订单状态
        if self.sync_status == "Pending":
            self.sync_with_etsy()

    def sync_with_etsy(self):
        """
        同步订单信息并更新状态。
        """
        try:
            order_details = fetch_etsy_order_details(self.etsy_order_id)
            self.update_order_details(order_details)
            self.sync_status = "Synced"
        except Exception as e:
            self.sync_status = "Error"
            frappe.log_error(f"Failed to sync order {self.etsy_order_id}: {e}")
            frappe.throw("Unable to synchronize order. Please check logs for details.")

    def update_order_details(self, order_details):
        """
        更新订单详细信息。
        """
        self.buyer_name = order_details.get("buyer_name", "")
        self.buyer_email = order_details.get("buyer_email", "")
        self.order_total = order_details.get("order_total", 0.0)
        self.order_date = order_details.get("order_date", "")
        self.shipping_address = order_details.get("shipping_address", "")
        self.tracking_number = order_details.get("tracking_number", "")
        # 更新订单项目
        self.items = []
        for item in order_details.get("items", []):
            self.append("items", {
                "item_name": item.get("item_name", ""),
                "quantity": item.get("quantity", 1),
                "price": item.get("price", 0.0)
            })
