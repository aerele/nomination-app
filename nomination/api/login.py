
import frappe


@frappe.whitelist(allow_guest=True)
def user_validation(mobile_number):
    user = frappe.db.get_value("User", {"mobile_no": mobile_number}, "name")
    if not user:
        return {"status": 0, "msg": "Mobile number not registered"}
    return {"status": 1, "msg": "User Registered"}


@frappe.whitelist(allow_guest=True)
def verify_otp(mobile_no ,otp):
    if (otp == "123456"):
        user = frappe.db.get_value("User", {"mobile_no": mobile_no}, "name")
        if not user:
            return {"status": 0, "msg": "User not found"}
        
        frappe.local.login_manager.user = user
        frappe.local.login_manager.post_login()
        
        return {"status": 1, "msg": "Logged in successfully", "user": user}
    
    
@frappe.whitelist()
def regenerate_sid():
    user = frappe.session.user
    frappe.local.login_manager.user = user
    frappe.local.login_manager.post_login()

    return {"status": 1, "msg": "Logged in successfully", "user": user}