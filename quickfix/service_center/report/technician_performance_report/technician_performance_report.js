// Copyright (c) 2026, Bhavathariniya and contributors
// For license information, please see license.txt

frappe.query_reports["Technician Performance Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			reqd: 1,
		},

		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			reqd: 1,
		},

		{
			fieldname: "technician",
			label: "Technician",
			fieldtype: "Link",
			options: "Technician",
		},
	],
};
