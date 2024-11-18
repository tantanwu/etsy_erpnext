app_name = "etsy_erpnext"
app_title = "Etsy ERPNext Integration"
app_publisher = "Jerry"
app_description = "A module for integrating Etsy with ERPNext."
app_icon = "octicon octicon-gear"
app_color = "blue"
app_email = "jerry@alstars.cn"
app_license = "MIT"

# Include JS, CSS files in header of desk.html (if needed)
# app_include_js = "/assets/etsy_erpnext/js/etsy_erpnext.js"
# app_include_css = "/assets/etsy_erpnext/css/etsy_erpnext.css"

# Include JS, CSS files in header of web template (if needed)
# web_include_js = "/assets/etsy_erpnext/js/etsy_erpnext.js"
# web_include_css = "/assets/etsy_erpnext/css/etsy_erpnext.css"

# Document Events: Hook on document methods and events
doc_events = {
    "Etsy Authorization": {
        "on_update": "etsy_erpnext.api.etsy_api.update_authorization_token",
    }
}

# Scheduler Events
scheduler_events = {
    "hourly": [
        "etsy_erpnext.tasks.sync_tasks.hourly_sync_etsy_orders"
    ]
}

# Override whitelisted methods (optional)
# override_whitelisted_methods = {
#     "method_name": "etsy_erpnext.api.etsy_api.synchronize_etsy_orders"
# }

# User Data Protection
user_data_fields = [
    {
        "doctype": "Etsy Authorization",
        "filter_by": "owner",
        "redact_fields": ["access_token", "refresh_token"],
        "partial": 1,
    }
]

# Authentication and authorization (if needed)
# auth_hooks = [
#     "etsy_erpnext.auth.validate"
# ]
