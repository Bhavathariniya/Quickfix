import frappe
from frappe import _

from quickfix.monkey_patches import apply_all


def run_after_install():
	after_install()
	apply_all()


def after_install():
	frappe.make_property_setter("Job Card", "remarks", "bold", 1, "Check")

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

	frappe.msgprint(_("QuickFix setup completed successfully"))


def before_uninstall():
	exists = frappe.db.exists("job Card", {"docstatus": 1})

	if exists:
		frappe.throw(_("Cannot uninstall: Submitted Job Cards exist", frappe.ValidationError))
