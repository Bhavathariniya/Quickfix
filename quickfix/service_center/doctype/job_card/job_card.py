# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_phone_number


class JobCard(Document):
	def before_insert(self):
		def_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

		if def_charge:
			self.labour_charge = def_charge

	def validate(self):
		if not validate_phone_number(self.customer_phone):
			frappe.throw(_("Invaild Mobile Number"))

		if self.status in ["In Repair", "Ready for Delivery", "Delivered", "Cancelled"]:
			if not self.assigned_technician:
				frappe.throw(_("Assigned Technician is required"))

			if not frappe.db.exists("Technician", self.assigned_technician):
				frappe.throw(_("Invalid Technician selected"))

		parts_total = 0

		for row in self.parts_used or []:
			row.total_price = (row.quantity or 0) * (row.unit_price or 0)
			parts_total += row.total_price

		self.parts_total = parts_total

		if not self.labour_charge:
			labour = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")
			self.labour_charge = labour or 0

		self.final_amount = (self.parts_total or 0) + (self.labour_charge or 0)

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Job Card can only be submitted when status is 'Ready for Delivery'"))

		for i in self.parts_used or []:
			stock_qty = frappe.db.get_value("Spare Parts", i.part, "stock_qty")

			if stock_qty is None:
				frappe.throw(_(f"Stock not found for part: {0}".format(i.part)))

			if stock_qty < (i.quantity or 0):
				frappe.throw(
					_(f"Insufficient stock for part {0}. Available: {1}, Required: {2}").format(
						i.part, stock_qty, i.quantity
					)
				)


@frappe.whitelist()
def share_job_card(job_card_name: str, user_email: str) -> dict:
	if not frappe.db.exists("Job Card", job_card_name):
		frappe.throw(_("Job Card not found"))

	if not frappe.db.exists("User", user_email):
		frappe.throw(_("User not found"))

	frappe.share.add(doctype="Job Card", name=job_card_name, user=user_email, read=1)

	return {"message": _("Job Card shared successfully")}


def get_permission_query_conditions(user):
	if not user:
		frappe.session.user

	roles = frappe.get_roles(user)

	if "QF Manager" in roles or "Administrator" == user:
		return None

	if "QF Technician" in roles:
		return f"""`tabJob Card`.assigned_technician IN
		(SELECT name FROM `tabTechnician` WHERE user = {frappe.db.escape(user)})"""

	return None
