frappe.listview_settings["Job Card"] = {
	add_fields: ["final_amount", "priority", "status"],

	get_indicator(doc) {
		if (doc.status === "Pending Diagnosis") {
			return ["Pending Diagnosis", "orange", "status,=,Pending Diagnosis"];
		} else if (doc.status === "In Repair") {
			return ["In Repair", "blue", "status,=,In Repair"];
		} else if (doc.status === "Ready for Delivery") {
			return ["Ready for Delivery", "green", "status,=,Ready for Delivery"];
		}
	},

	formatters: {
		final_amount(values) {
			return format_currency(values);
		},
	},

	button: {
		show(doc) {
			return doc.status === "In Repair";
		},

		get_label() {
			return "Complete Repair";
		},

		get_description(doc) {
			return `Complete ${doc.name}`;
		},

		action(doc) {
			frappe.call({
				method: "quickfix.api.complete_repair",
				args: {
					job_card: doc.name,
				},
				callback() {
					frappe.show_alert("Repair Completed");

					frappe.listview.refresh();
				},
			});
		},
	},
};
