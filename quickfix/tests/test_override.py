import unittest

import frappe


class TestOverride(unittest.TestCase):
	# def test_override_called(self):
	#     frappe.set_user("Administrator")

	#     frappe.call("frappe.client.get_count",doctype="Job Card")

	#     log = frappe.get_all("Audit Log",
	#         filters = {"action":"count_queried"},fields=["name"])

	#     self.assertTrue(len(log)>0)

	def test_original_logic(self):
		count1 = frappe.db.count("Job Card")

		count2 = frappe.call("frappe.client.get_count", doctype="Job Card")

		self.assertEqual(count1, count2)

	# def test_no_break(self):
	#     result = frappe.call("frappe.client.get_count",doctype="User")

	#     self.assertIsInstance(result,int)
