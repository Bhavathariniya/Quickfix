# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	pass


def has_permission(doc, user=None):
	if not user:
		frappe.session.user

	role = frappe.get_roles(user)

	if "QF Manager" in role or user == "Administrator":
		return None

	payment_status = frappe.db.get_value("Job Card", doc.job_card, "payment_status")

	return payment_status == "Paid"
