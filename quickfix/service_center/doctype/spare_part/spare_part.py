# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def autoname(self):
		if self.part_code:
			self.part_code = self.part_code.upper()

		# self.name = make_autoname("PART-.YYYY.-.####")
		self.name = make_autoname(self.naming_series)

	def validate(self):
		if self.selling_price <= self.unit_cost:
			frappe.throw(_("Selling price must be greater than unit cost"))

	def on_update(self):
		threshold = frappe.db.get_single_value("QuickFix Settings", "low_stock_threshold")
		if self.stock_qty < threshold:
			frappe.msgprint(_("Stock is below threshold"))
