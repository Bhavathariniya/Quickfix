"""
MONKEY PATCHES FOR QUICKFIX APP
=================================

Each patch documents:
- WHY it exists
- WHAT it changes
- VERSION tested
- RISK of future breakage
- TEST coverage
"""

import frappe


def apply_all():
	_patch_get_url()


def _patch_get_url():
	"""
	WHY:
	    Site requires custom CDN prefix support.

	WHAT:
	    Prepends custom_url_prefix to generated URLs.

	VERSION TESTED:
	    Frappe v15.x

	RISK:
	    If frappe.utils.get_url changes signature,
	    this patch may fail.

	TEST:
	    test_monkey_patches.py::TestGetUrl
	"""

	import frappe.utils as fu

	# Prevent double patching
	if hasattr(fu, "_qf_patched"):
		return

	# Save original function
	_orig = fu.get_url

	# Custom wrapper
	def _custom_get_url(path=None, full_address=False):
		url = _orig(path, full_address)

		prefix = frappe.conf.get("custom_url_prefix", "")

		return prefix + url if prefix else url

	# Replace original function
	fu.get_url = _custom_get_url

	# Guard flag
	fu._qf_patched = True
