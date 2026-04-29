# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def before_insert(self):
		def_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

		if def_charge:
			self.labour_charge = def_charge

	@frappe.whitelist()
	def share_job_card(job_card_name: str, user_email: str) -> dict:
		if not frappe.db.exists("Job Card", job_card_name):
			frappe.throw(_("Job Card not found"))

		if not frappe.db.exists("User", user_email):
			frappe.throw(_("User not found"))

		frappe.share.add(doctype="Job Card", name=job_card_name, user=user_email, read=1)

		return {"message": _("Job Card shared successfully")}
