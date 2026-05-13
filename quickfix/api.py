import hashlib
import hmac
import json
import time

import frappe
import requests
from frappe import _
from frappe.client import get_count
from frappe.utils import now, now_datetime, today

frappe.utils.logger.set_log_level("INFO")


logger = frappe.logger("quickfix", allow_site=True, file_count=5)


@frappe.whitelist()
def manager_only_action():
	frappe.only_for("QF Manager")

	return {"you're allowed to use this method"}


# def log_change(doc, method):
# 	try:
# 		frappe.get_doc({
# 			"doctype": "Audit Log"
# 		})


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


# This method is intentionally unsafe for demonstration purposes
# It uses get_all() which bypasses permission_query_conditions
# and should NEVER be exposed with allow_guest=True in production


# @frappe.whitelist(allow_guest=True)
@frappe.whitelist()
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
def send_job_ready_email(job_card: str) -> None:
	frappe.logger().info(f"Sending email for {job_card}")

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


@frappe.whitelist()
def rename_technician(old_name: str, new_name: str) -> str:
	# merge=True is dangerous because it combines two documents into one.
	# If the records are not true duplicates, it can overwrite data,
	# corrupt relationships, and cause incorrect linkage in other documents.
	# It should only be used when both records represent the same entity.

	frappe.rename_doc("Technician", old_name, new_name, merge=False)

	return f"Technician renamed from {old_name} to {new_name}"


def validate_job_card(doc, method):
	if not doc.customer_phone:
		frappe.throw(_("Phone required (doc_events)"))

	print("docevent validate")


@frappe.whitelist()
def custom_get_count(
	doctype: str, filters: dict | list | None = None, debug: bool = False, cache: bool = False
) -> int:
	frappe.logger().info("OVERRIDE HIT")

	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doctype,
			"action": "count_queried",
			"user": frappe.session.user,
		}
	).insert(ignore_permissions=True)

	return get_count(doctype, filters, debug, cache)


@frappe.whitelist()
def mark_delivered(job_card: str):
	doc = frappe.get_doc("Job Card", job_card)

	if doc.status != "Ready for Delivery":
		frappe.throw(_("Only Ready for Delivery jobs can be delivered"))

	doc.db_set("status", "Delivered")

	doc.save()

	return "Success"


@frappe.whitelist()
def reject_job(job_card: str, reason: str):
	doc = frappe.get_doc("Job Card", job_card)

	if doc.docstatus == 1:
		frappe.throw(_("Submitted Job Cards cannot be rejected"))

	doc.db_set("status", "Cancelled")

	doc.add_comment("Comment", f"Rejected Reason: {reason}")

	doc.save()

	return "Success"


@frappe.whitelist()
def complete_repair(job_card: str):
	doc = frappe.get_doc("Job Card", job_card)

	if doc.status != "In Repair":
		frappe.throw(_("Only In Repair jobs can be completed"))

	doc.db_set("status", "Ready for Delivery")

	doc.save()

	return "Success"


@frappe.whitelist()
def transfer_technician(job_card: str, technician: str):
	doc = frappe.get_doc("Job Card", job_card)

	doc.assigned_technician = technician

	doc.save()

	return "Success"


# @frappe.whitelist()
# def get_status_chart_data():
# 	data = frappe.db.sql(
# 		"""

#         SELECT
#             status,
#             COUNT(*) as count

#         FROM `tabJob Card`

#         GROUP BY status

#     """,
# 		as_dict=True,
# 	)

# 	return {
# 		"labels": [d.status for d in data],
# 		"datasets": [{"name": "Jobs", "values": [d.count for d in data]}],
# 	}


# def check_low_stock():

#     last_run = frappe.db.exists(

#         "Audit Log",

#         {

#             "action": "low_stock_check",

#             "creation": ["like", f"{today()}%"]

#         }

#     )

#     if last_run:

#         return


#     frappe.get_doc({

#         "doctype": "Audit Log",

#         "action": "low_stock_check"

#     }).insert(ignore_permissions=True)


#     low_stock_parts = frappe.get_all(

#         "Spare Part",

#         filters={

#             "stock_qty": ["<=", "reorder_level"]

#     },

#     fields=[

#         "name",
#         "stock_qty",
#         "reorder_level"

#     ]

# )

# frappe.logger().info(

#     f"Low stock parts: {low_stock_parts}"

# )


def check_low_stock():
	cache_key = f"low_stock_check_{today()}"

	if frappe.cache().get_value(cache_key):
		print("Already Ran Today")

		return

	frappe.cache().set_value(cache_key, True)

	print("Running Low Stock Check")

	low_stock_parts = frappe.get_all(
		"Spare Part",
		filters={"stock_qty": ["<=", "reorder_level"]},
		fields=["name", "stock_qty", "reorder_level"],
	)

	print(low_stock_parts)


def generate_monthly_revenue_report(year):
	months = range(1, 13)

	total_revenue = 0

	for i, month in enumerate(months, 1):
		revenue = (
			frappe.db.sql(
				"""

            SELECT
                SUM(final_amount)

            FROM `tabJob Card`

            WHERE
                status = 'Delivered'
                AND YEAR(modified) = %s
                AND MONTH(modified) = %s

        """,
				(year, month),
			)[0][0]
			or 0
		)

		total_revenue += revenue

		frappe.publish_progress(
			percent=round(i / 12 * 100),
			title="Generating Revenue Report",
			description=f"Processing month {month}...",
		)

		time.sleep(1)

	frappe.logger().info(f"Revenue Report Generated " f"for {year} : {total_revenue}")
	print(f"Revenue Report Generated for {year}")
	return total_revenue


@frappe.whitelist()
def trigger_ready_email(job_card: str):
	frappe.enqueue("quickfix.api.send_job_ready_email", queue="short", job_card=job_card)


@frappe.whitelist()
def trigger_revenue_report(year: int):
	frappe.enqueue("quickfix.api.generate_monthly_revenue_report", queue="long", timeout=600, year=year)


def failing_background_job():
	frappe.logger().info("Failing job started")

	raise Exception("Intentional Background Job Failure")


def monthly_report_scheduler():
	year = now_datetime().year

	frappe.enqueue("quickfix.api.generate_monthly_revenue_report", queue="long", timeout=600, year=year)


@frappe.whitelist()
def trigger_failed_job():
	frappe.enqueue("quickfix.api.failing_background_job", queue="default")

	frappe.msgprint(_("Failing job queued"))


# def cancel_old_draft_jobs():
# 	frappe.db.sql("""UPDATE `tabJob Card` SET status = 'cancelled'
# 				  WHERE docstatus = 0 AND creation < DATE_SUB(NOW(),INTERVAL 30 DAY) """)

# 	frappe.db.commit()


def bulk_insert_logs():
	rows = []

	for _i in range(500):
		rows.append((frappe.generate_hash(), frappe.session.user, "Bulk Insert Test"))

	frappe.db.bulk_insert("Audit Log", fields=["name", "owner", "action"], values=rows)

	print("bulk insert running")


def send_webhook(job_card_name, retry_count=0):
	logger.info(f"Webhook started for {job_card_name}")
	logger.warning("Webhook called")
	settings = frappe.get_single("QuickFix Settings")

	if not settings.webhook_url:
		logger.warning("Webhook not configured")

		return

	doc = frappe.get_doc("Job Card", job_card_name)

	webhook_id = hashlib.sha256(f"{doc.name}-job_submitted".encode()).hexdigest()

	existing = frappe.db.exists("Audit Log", {"method": webhook_id})

	if existing:
		return

	payload = {
		"event": "job_submitted",
		"ref": doc.name,
		"customer": doc.customer_name,
		"amount": doc.final_amount,
	}

	payload_json = json.dumps(payload).encode()

	secret = frappe.conf.get("payment_webhook_secret", "")

	signature = hmac.new(secret.encode(), payload_json, hashlib.sha256).hexdigest()

	try:
		logger.info(f"Sending webhook for {doc.name}")

		r = requests.post(
			settings.webhook_url,
			data=payload_json,
			headers={"Content-Type": "application/json", "X-Signature": signature},
			timeout=5,
		)

		r.raise_for_status()

		# system action, not user-initiated so ignore permission is true

		frappe.get_doc(
			{
				"doctype": "Audit Log",
				"method": webhook_id,
				"reference_doctype": "Job Card",
				"document_name": doc.name,
			}
		).insert(ignore_permissions=True)

	except Exception as e:
		frappe.log_error(f"Webhook failed: {e}", "Webhook Error")

		if retry_count < 3:
			frappe.enqueue(
				"quickfix.api.send_webhook",
				queue="short",
				enqueue_after_commit=True,
				job_card_name=job_card_name,
				retry_count=retry_count + 1,
				at_front=False,
			)


# @frappe.whitelist(allow_guest=True)
@frappe.whitelist()
def payment_webhook():
	payload = frappe.request.data

	secret = frappe.conf.get("payment_webhook_secret", "")

	signature = frappe.get_request_header("X-Signature")

	expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

	if not hmac.compare_digest(expected, signature or ""):
		frappe.throw(_("Invalid signature", frappe.AuthenticationError))

	data = json.loads(payload)

	exists = frappe.db.exists("Audit Log", {"action": "payment_received", "document_name": data["ref"]})

	if exists:
		return {"status": "duplicate", "message": "Already processed"}

	frappe.db.set_value("Job Card", data["ref"], "payment_status", "Paid")

	# ignore_permissions=True is acceptable here because:
	# This stock deduction is a SYSTEM-INITIATED operation triggered by document submission,
	# not a direct user action.

	frappe.get_doc(
		{"doctype": "Audit Log", "action": "payment_received", "document_name": data["ref"]}
	).insert(ignore_permissions=True)

	return {"status": "ok"}


@frappe.whitelist()
def get_status_chart_data():
	cache_key = "quickfix_status_chart"

	cached = frappe.cache().get_value(cache_key)

	if cached:
		return cached

	data = frappe.db.sql(
		"""

		SELECT

			status,

			COUNT(name) as count

		FROM `tabJob Card`

		GROUP BY status

	""",
		as_dict=True,
	)

	result = {
		"labels": [d.status for d in data],
		"datasets": [{"name": "Jobs", "values": [d.count for d in data]}],
	}

	frappe.cache().set_value(cache_key, result, expires_in_sec=300)

	return result
