import frappe


def get_context(context):
	job_id = frappe.form_dict.get("job_id")

	if job_id:
		job = frappe.db.get_value("Job Card", job_id, ["status", "customer_name"], as_dict=True)

		context.job = job
		print(job)
		context.job_id = job_id

	return context
