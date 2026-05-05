# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class AuditLog(Document):
	pass


def log_change(doc, method):
	# ⚠️ Prevent infinite loop
	if doc.doctype == "Audit Log":
		return

	try:
		frappe.get_doc(
			{
				"doctype": "Audit Log",
				"doctype_name": doc.doctype,
				"document_name": doc.name,
				"action": method,
				"user": frappe.session.user,
				"timestamp": now(),
			}
		).insert(ignore_permissions=True)

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Audit Log Failed")
