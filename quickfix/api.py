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
