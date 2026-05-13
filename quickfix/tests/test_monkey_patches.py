import unittest

import frappe

from quickfix.monkey_patches import apply_all


class TestGetUrl(unittest.TestCase):
	def setUp(self):
		apply_all()

	def test_with_prefix(self):
		frappe.conf.custom_url_prefix = "https://cdn.test.com"

		url = frappe.utils.get_url("/files/test.png")

		self.assertTrue(url.startswith("https://cdn.test.com"))

	def test_without_prefix(self):
		frappe.conf.custom_url_prefix = ""
		url = frappe.utils.get_url("/files/test.png")

		self.assertFalse(url.startswith("https://cdn.test.com"))
