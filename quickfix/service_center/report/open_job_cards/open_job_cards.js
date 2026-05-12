frappe.query_reports["Open Job Cards"] = {
	filters: [
		{
			fieldname: "device_type",
			label: "Device Type",
			fieldtype: "Link",
			options: "Device Type",
			default: "Smart Phone",
		},
	],

	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "completion_rate") {
			if (data.completion_rate < 70) {
				value = `<span style="color:red;font-weight:bold">${value}</span>`;
			} else if (data.completion_rate >= 90) {
				value = `<span style="color:green;font-weight:bold">${value}</span>`;
			}
		}

		return value;
	},
};
