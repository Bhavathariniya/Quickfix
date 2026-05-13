// Copyright (c) 2026, Bhavathariniya and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (data && data.stock_qty <= data.reorder_level) {
			value = `
                <span style="
                    background-color:#ffcccc;
                    font-weight:bold;
                ">
                    ${value}
                </span>
            `;
		}

		return value;
	},
};
