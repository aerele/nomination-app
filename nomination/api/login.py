import frappe

from nomination.api.rangde_service import get_tokens, initiate_session, request_otp, verify_otp


@frappe.whitelist(allow_guest=True)
def user_validation(mobile_number):
	user = frappe.db.get_value("User", {"mobile_no": mobile_number}, "name")
	if not user:
		return {"status": 0, "msg": "Mobile number not registered"}

	auth_token, csrf_token = get_tokens()

	if not auth_token or not csrf_token:
		initiate_session()

	send_otp(mobile_number)

	return {"status": 1, "msg": "OTP sent successfully"}


@frappe.whitelist(allow_guest=True)
def send_otp(mobile_number):
	result = request_otp(mobile_number)

	return {"status": 1, "msg": result}


@frappe.whitelist(allow_guest=True)
def verify_user_otp(mobile_number, otp):
	result = verify_otp(mobile_number, otp)

	messages = result.get("messages", [])

	if not messages or messages[0].get("code") != "1":
		return {"status": 0, "msg": "OTP verification failed"}
