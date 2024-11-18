from frappe.utils.background_jobs import enqueue
from etsy_erpnext.api.etsy_api import synchronize_etsy_orders

def hourly_sync_etsy_orders():
    """
    Task to synchronize Etsy orders hourly.
    This function is scheduled to run every hour.
    """
    enqueue(
        method=sync_etsy_orders_task,
        queue="long",
        timeout=300,
        is_async=True,
    )

def sync_etsy_orders_task():
    """
    Core function that handles Etsy order synchronization.
    This function calls `synchronize_etsy_orders` from the Etsy API module.
    """
    try:
        synchronize_etsy_orders()
    except Exception as e:
        frappe.log_error(message=str(e), title="Etsy Order Synchronization Failed")
        raise
