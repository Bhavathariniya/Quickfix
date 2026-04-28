# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	

	def before_insert(self):

		def_charge = frappe.db.get_single_value("QuickFix Settings","default_labour_charge")
		
		if def_charge:
			self.labour_charge = def_charge
