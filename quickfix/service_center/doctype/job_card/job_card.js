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
		if (frm.doc.status === "Pending Diagnosis") {
			frm.dashboard.add_indicator("Pending Diagnosis", "orange");
		} else if (frm.doc.status === "In Repair") {
			frm.dashboard.add_indicator("In Repair", "blue");
		} else if (frm.doc.status === "Ready for Delivery") {
			frm.dashboard.add_indicator("Ready for Delivery", "green");
		}

		if (frm.frm.doc.status === "ready for Delivery" && frm.doc.docstatus === 1) {
			frm.add_custom_button("Mark as Delivered", () => {
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

		if (frm.boot.quickfix_shop_name) {
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

				let specialization = r.message;

				if (specialization && specialization !== frm.doc.device_type) {
					frappe.msgprint("Technician specialization does not match device type");
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
