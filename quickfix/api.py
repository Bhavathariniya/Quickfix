import frappe
from frappe import _


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


@frappe.whitelist()
def send_job_ready_email(job_card):
	doc = frappe.get_doc("Job Card", job_card)

	recipient = doc.customer_email or frappe.db.get_value("User", doc.owner, "email")

	if not recipient:
		frappe.log_error("No recipient found for Job Ready Email", "Email Error")
		return

	subject = _("Your Device is Ready for Delivery")

	message = f"""
        <p>Hello,</p>
        <p>Your device for Job Card <b>{doc.name}</b> is ready for delivery.</p>
        <p>Total Amount: <b>{doc.final_amount}</b></p>
        <p>Please visit our service center to collect your device.</p>
        <br>
        <p>Thank you,<br>QuickFix Team</p>
    """

	frappe.sendmail(recipients=[recipient], subject=subject, message=message)
