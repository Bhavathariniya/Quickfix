// Copyright (c) 2026, Bhavathariniya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	setup(frm) {
		frm.set_query("assigned_technician", () => {
			return {
				filters: {
					status: "Active",
					specialization: frm.doc.device_type,
				},
			};
		});
	},

	onload(frm) {
		if (!frm.job_ready_listener_added) {
			frappe.realtime.on("job_ready", (data) => {
				if (data.job_card === frm.doc.name) {
					frappe.msgprint({
						title: "Job Ready",
						message: `Job Card ${data.job_card} is ready for delivery`,
						indicator: "green",
					});
				}
			});

			frm.job_ready_listener_added = true;
		}
	},

	refresh(frm) {
		if (!frappe.user.has_role("QF Manager")) {
			frm.set_df_property("customer_phone", "hidden", 1);
		}

		frm.add_custom_button(
			__("Generate Revenue Report"),

			() => {
				frappe.call({
					method: "quickfix.api.trigger_revenue_report",

					args: {
						year: 2026,
					},

					callback() {
						frappe.msgprint(__("Report generation started"));
					},
				});
			}
		);

		frm.add_custom_button(__("Transfer Technician"), () => {
			frappe.prompt(
				[
					{
						label: __("New Technician"),
						fieldname: "technician",
						fieldtype: "Link",
						options: "Technician",
						reqd: 1,
					},
				],

				(values) => {
					frappe.confirm(`Transfer to ${values.technician}?`, () => {
						frappe.call({
							method: "quickfix.api.transfer_technician",
							args: {
								job_card: frm.doc.name,
								technician: values.technician,
							},
							callback() {
								frm.set_value("assigned_technician", values.technician);

								frm.trigger("assigned_technician");

								frappe.msgprint(__("Technician Transfered"));
							},
						});
					});
				},

				"Transfer Technician",
				"Transfer"
			);
		});

		frm.add_custom_button(__("Reject Job"), () => {
			let d = new frappe.ui.Dialog({
				title: __("Reject Job"),

				fields: [
					{
						label: __("Rejection Reason"),
						fieldname: "reason",
						fieldtype: "Small Text",
						reqd: 1,
					},
				],

				primary_action_label: "Reject",

				primary_action(values) {
					frappe.call({
						method: "quickfix.api.reject_job",
						args: {
							job_card: frm.doc.name,
							reason: values.reason,
						},

						callback() {
							frappe.msgprint(__("Job Rejected"));
							frm.reload_doc();
						},
					});

					d.hide();
				},
			});

			d.show();
		});

		if (frm.doc.status === "Pending Diagnosis") {
			frm.dashboard.add_indicator("Pending Diagnosis", "orange");
		} else if (frm.doc.status === "In Repair") {
			frm.dashboard.add_indicator("In Repair", "blue");
		} else if (frm.doc.status === "Ready for Delivery") {
			frm.dashboard.add_indicator("Ready for Delivery", "green");
		}

		if (frm.doc.status === "Ready for Delivery" && frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Mark as Delivered"), () => {
				frappe.call({
					method: "quickfix.api.mark_delivered",
					args: {
						job_card: frm.doc.name,
					},
					callback() {
						frm.reload_doc();
					},
				});
			});
		}

		if (frappe.boot.quickfix_shop_name) {
			frm.page.set_indicator(frappe.boot.quickfix_shop_name, "blue");
		}
	},

	assigned_technician(frm) {
		if (!frm.doc.assigned_technician) {
			return;
		}

		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Technician",
				name: frm.doc.assigned_technician,
			},
			callback(r) {
				if (!r.message) {
					return;
				}

				let specialization = r.message.specialization;

				if (specialization && specialization != frm.doc.device_type) {
					frappe.msgprint(__("Technician specialization does not match device type"));
				}
			},
		});
	},
});

frappe.ui.form.on("Part Usage Entry", {
	quantity(frm, cdt, cdn) {
		calculate_total(cdt, cdn);
	},
	unit_price(frm, cdt, cdn) {
		calculate_total(cdt, cdn);
	},
});

function calculate_total(cdt, cdn) {
	let row = frappe.get_doc(cdt, cdn);
	let total = (row.quantity || 0) * (row.unit_price || 0);

	frappe.model.set_value(cdt, cdn, "total_price", total);
}
