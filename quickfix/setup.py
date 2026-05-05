import frappe


def after_install():
	device_types = ["Mobile", "Laptop", "Tablet"]

	for dt in device_types:
		if not frappe.db.exists("Device Type", dt):
			frappe.get_doc({"doctype": "Device Type", "device_type_name": dt}).insert(ignore_permissions=True)

	if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
		frappe.get_doc(
			{
				"doctype": "QuickFix Settings",
				"shop_name": "Service Center",
				"manager_email": "bhavathariniya13@gmail.com",
				"low_stock_threshold": 5,
			}
		).insert(ignore_permissions=True)

	frappe.msgprint("QuickFix setup completed successfully")


def before_uninstall():
	exists = frappe.db.exists("job Card", {"docstatus": 1})

	if exists:
		frappe.throw("Cannot uninstall: Submitted Job Cards exist", frappe.ValidationError)
