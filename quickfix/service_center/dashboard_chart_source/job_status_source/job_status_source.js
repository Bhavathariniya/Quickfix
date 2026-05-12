frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Job Status Source"] = {
	method: "quickfix.api.get_status_chart_data",
};
