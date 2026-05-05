import unittest

import frappe


class TestJobCard(unittest.TestCase):
	def test_validate_calls_super(self):
		doc = frappe.get_doc(
			{
				"doctype": "Job Card",
				"customer_name": "Test",
				"customer_phone": "123",
				"device_type": "Smartphone",
				"problem_description": "display broke",
				"status": "Draft",
			}
		)

		with self.assertRaises(frappe.ValidationError):
			doc.insert()


# import frappe
# import unittest


# class TestJobCard(unittest.TestCase):

#     def test_validate_calls_super(self):

#         doc = frappe.get_doc({
#             "doctype": "Job Card",
#             "customer_name": "Test",
#             "customer_phone": "123",
#             "status": "Draft"
#         })

#         # Expect validation error
#         with self.assertRaises(frappe.ValidationError):
#             doc.insert()
