import frappe


@frappe.whitelist()
def manager_only_action():
	frappe.only_for("QF Manager")

	return {"you're allowed to use this method"}


def get_permission_query_conditions(user: str | None):
	if not user:
		frappe.session.user

	roles = frappe.get_roles(user)

	if "QF Manager" in roles or user == "Administrator":
		return None

	if "QF Technician" in roles:
		return f"""
            `tabTechnician`.user = {frappe.db.escape(user)}
        """

	return None


@frappe.whitelist(allow_guest=True)
def get_job_cards_Unsafe_fn():
	return frappe.get_all("Job Card", fields=["*"])


@frappe.whitelist()
def get_job_cards_Safe_fn():
	user = frappe.session.user
	roles = frappe.get_roles(user)

	data = frappe.get_list(
		"Job Card",
		fields=[
			"name",
			"customer_name",
			"status",
			"assigned_technicians",
			"customer_phone",
			"customer_email",
		],
	)

	if "QF Manager" not in roles and user != "Administrator":
		for d in data:
			d.pop("customer_phone", None)
			d.pop("customer_email", None)

	return data
