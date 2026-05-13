import frappe
from frappe.utils import now


def on_login(login_manager):
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": "User",
			"document_name": login_manager.user,
			"action": "login",
			"user": login_manager.user,
			"timestamp": now(),
		}
	).insert(ignore_permissions=True)


def on_logout(login_manager):
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": "User",
			"document_name": login_manager.user,
			"action": "logout",
			"user": login_manager.user,
			"timestamp": now(),
		}
	).insert(ignore_permissions=True)
