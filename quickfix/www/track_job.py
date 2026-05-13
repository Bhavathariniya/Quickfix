import re

import frappe


def get_context(context):
	phone = frappe.form_dict.get("phone", "")

	# sanitize the input

	phone = re.sub(r"\D", "", phone)

	if len(phone) > 10:
		phone = phone[:10]

	context.phone = phone

	if len(phone) != 10:
		return context

	# Rate limiting

	ip = frappe.local.request_ip

	cache_key = f"track_job:{ip}"

	count = frappe.cache.get_value(cache_key) or 0

	if int(count) >= 20:
		frappe.throw("Too many requests. Try again later.")

	frappe.cache.set_value(cache_key, int(count) + 1, expires_in_sec=60)

	# fetch jobs

	jobs = frappe.get_list(
		"Job Card",
		filters={"customer_phone": phone},
		fields=["name", "status", "device_brand"],
		limit_page_length=10,
	)

	context.jobs = jobs

	return context


# ------------------------------------------------------------
# using Job Id
# ------------------------------------------------------------
# def get_context(context):
# 	job_id = frappe.form_dict.get("job_id")

# 	if job_id:
# 		job = frappe.db.get_value("Job Card", job_id, ["status", "customer_name"], as_dict=True)

# 		context.job = job
# 		print(job)
# 		context.job_id = job_id

# 	return context
