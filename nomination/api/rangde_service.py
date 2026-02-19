import frappe
import requests

BASE_URL = "https://mercury.rangde.in/core/api"
TIMEOUT = 10


def get_api_key():
	api_key = frappe.conf.get("rangde_api_key")
	if not api_key:
		frappe.throw("RangDe API key not configured")
	return api_key


def initiate_session():
	url = f"{BASE_URL}/login"

	headers = {"x-rang-de": get_api_key()}

	response = requests.get(url, headers=headers, timeout=TIMEOUT)

	if response.status_code != 200:
		frappe.throw("Failed to initiate RangDe session")

	auth_token = response.headers.get("x-auth-token")
	csrf_token = response.headers.get("x-csrf-token")

	if not auth_token or not csrf_token:
		frappe.throw("RangDe tokens missing")

	frappe.cache().set_value("rangde_auth_token", auth_token)
	frappe.cache().set_value("rangde_csrf_token", csrf_token)

	return auth_token, csrf_token


def get_tokens():
	cached_auth_token = frappe.cache().get_value("rangde_auth_token")
	cached_csrf_token = frappe.cache().get_value("rangde_csrf_token")

	if not cached_auth_token or not cached_csrf_token:
		return initiate_session()

	return cached_auth_token, cached_csrf_token


def _post(endpoint, data, retry=True):
	auth_token, csrf_token = get_tokens()

	headers = {
		"x-rang-de": get_api_key(),
		"x-auth-token": auth_token,
		"x-csrf-token": csrf_token,
		"Content-Type": "application/x-www-form-urlencoded",
	}

	url = f"{BASE_URL}/{endpoint}"

	response = requests.post(url, headers=headers, data=data, timeout=TIMEOUT)

	if response.status_code == 401 and retry:
		initiate_session()
		return _post(endpoint, data, retry=False)

	if response.status_code != 200:
		frappe.throw(f"RangDe API error: {response.text}")

	return response.json()


def request_otp(mobileNumber):
	mobilenumber = mobileNumber.strip()

	payload = {"mobileNumber": mobilenumber, "purpose": "NOMINATION"}

	return _post("otp/requests/general", payload)


def verify_otp(mobileNumber, otp):
	mobileNumber = mobileNumber.strip()

	payload = {"mobileNumber": mobileNumber, "code": otp}

	return _post("otp/requests/general/verify", payload)
