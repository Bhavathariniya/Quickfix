# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff


def execute(filters=None):
	columns = get_columns(filters)

	data = get_data(filters)

	chart = get_chart(data)

	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns(filters):
	columns = [
		{
			"label": _("Technician"),
			"fieldname": "technician",
			"fieldtype": "Link",
			"options": "Technician",
			"width": 180,
		},
		{"label": _("Total Jobs"), "fieldname": "total_jobs", "fieldtype": "Int", "width": 120},
		{"label": _("Completed"), "fieldname": "completed", "fieldtype": "Int", "width": 120},
		{"label": _("Avg Turnaround Days"), "fieldname": "avg_days", "fieldtype": "Float", "width": 160},
		{"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 140},
		{
			"label": _("Completion Rate %"),
			"fieldname": "completion_rate",
			"fieldtype": "Percent",
			"width": 150,
		},
	]

	for dt in frappe.get_all("Device Type", fields=["name"]):
		columns.append(
			{
				"label": dt.name,
				"fieldname": dt.name.lower().replace(" ", "_"),
				"fieldtype": "Int",
				"width": 100,
			}
		)

	return columns


def get_data(filters):
	conditions = {}

	if filters.get("technician"):
		conditions["assigned_technician"] = filters.get("technician")

	jobs = frappe.get_list(
		"Job Card",
		filters=conditions,
		fields=["assigned_technician", "status", "device_type", "final_amount", "creation", "modified"],
	)

	technician_map = {}

	for job in jobs:
		tech = job.assigned_technician or "Unassigned"

		if tech not in technician_map:
			technician_map[tech] = {
				"technician": tech,
				"total_jobs": 0,
				"completed": 0,
				"avg_days": 0,
				"revenue": 0,
				"completion_rate": 0,
			}

		row = technician_map[tech]

		row["total_jobs"] += 1

		if job.status == "Delivered":
			row["completed"] += 1

			row["revenue"] += job.final_amount or 0

		days = date_diff(job.modified, job.creation)

		row["avg_days"] += days

		fieldname = job.device_type.lower().replace(" ", "_")

		row[fieldname] = row.get(fieldname, 0) + 1

	data = []

	for row in technician_map.values():
		if row["total_jobs"]:
			row["avg_days"] /= row["total_jobs"]

			row["completion_rate"] = (row["completed"] / row["total_jobs"]) * 100

		data.append(row)

	return data


def get_chart(data):
	return {
		"data": {
			"labels": [d["technician"] for d in data],
			"datasets": [
				{"name": "Total Jobs", "values": [d["total_jobs"] for d in data]},
				{"name": "Completed", "values": [d["completed"] for d in data]},
			],
		},
		"type": "bar",
	}


def get_report_summary(data):
	total_jobs = sum(d["total_jobs"] for d in data)

	total_revenue = sum(d["revenue"] for d in data)

	best_tech = max(data, key=lambda d: d["completed"], default={})

	return [
		{"label": _("Total Jobs"), "value": total_jobs, "indicator": "blue"},
		{"label": _("Total Revenue"), "value": total_revenue, "indicator": "green"},
		{"label": _("Best Technician"), "value": best_tech.get("technician", ""), "indicator": "orange"},
	]
