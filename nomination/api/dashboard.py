import frappe


@frappe.whitelist()
def get_dashboard_data():
	user = frappe.session.user
	if user == "Guest":
		return {"status": 0, "msg": "User not logged in"}
	dashboard_data = frappe.get_list("Nomination Form", fields=["name", "status", "created_by"])
	return {"status": 1, "data": dashboard_data}
