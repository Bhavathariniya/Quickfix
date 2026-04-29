import frappe


@frappe.whitelist()
def perm_for_manager():
	frappe.only_for("QF Manager")
