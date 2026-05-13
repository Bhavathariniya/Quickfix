import base64
from io import BytesIO

import frappe
import qrcode


def get_shop_name():
	settings = frappe.get_single("QuickFix Settings")
	return settings.shop_name


def format_job_id(value):
	return f"JOB#{value}"


def get_qr_code(job_card):
	url = frappe.utils.get_url(f"/app/job-card/{job_card}")

	qr = qrcode.make(url)

	buffer = BytesIO()

	qr.save(buffer, format="PNG")

	img = base64.b64encode(buffer.getvalue()).decode()

	return "data:image/png;base64," + img
