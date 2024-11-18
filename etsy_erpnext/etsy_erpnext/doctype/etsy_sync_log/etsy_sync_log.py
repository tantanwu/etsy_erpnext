# etsy_erpnext/doctype/etsy_sync_log/etsy_sync_log.py

import frappe
from frappe.model.document import Document
from datetime import datetime

class EtsySyncLog(Document):
    """
    日志记录Etsy同步操作的详细信息。
    """

    def before_insert(self):
        """
        在创建日志条目之前自动填写时间和用户信息。
        """
        self.start_time = self.start_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.created_by = frappe.session.user or "System"

    def on_submit(self):
        """
        在提交日志时检查完成时间。
        """
        if not self.end_time:
            self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
