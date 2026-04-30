// Copyright (c) 2026, Bhavathariniya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	refresh(frm) {
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
});
