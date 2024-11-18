# etsy_erpnext/__init__.py

# 模块元信息
__version__ = "1.0.0"
__author__ = "Jerry"
__description__ = "A local ERPNext module for managing Etsy orders and authorization."

# 如果需要在模块初始化时加载工具或配置，可以导入
from .utils.etsy_utils import validate_etsy_authorization
from .tasks.sync_tasks import hourly_sync
