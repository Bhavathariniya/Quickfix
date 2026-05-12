# Copyright (c) 2026, Bhavathariniya and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()

	data = get_data()

	summary = get_summary(data)

	chart = None

	skip_total_row = False

	return (columns, data, None, chart, summary, skip_total_row)


def get_columns():
	return [
		{"label": _("Part Name"), "fieldname": "part_name", "fieldtype": "Data", "width": 180},
		{
			"label": _("Part Code"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Spare Part",
			"width": 140,
		},
		{
			"label": _("Device Type"),
			"fieldname": "device_type",
			"fieldtype": "Link",
			"options": "Device Type",
			"width": 140,
		},
		{"label": _("Stock Qty"), "fieldname": "stock_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Reorder Level"), "fieldname": "reorder_level", "fieldtype": "Float", "width": 130},
		{"label": _("Unit Cost"), "fieldname": "unit_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Selling Price"), "fieldname": "selling_price", "fieldtype": "Currency", "width": 130},
		{"label": _("Margin %"), "fieldname": "margin", "fieldtype": "Percent", "width": 120},
		{"label": _("Total Value"), "fieldname": "total_value", "fieldtype": "Currency", "width": 140},
	]


def get_data():
	parts = frappe.get_list(
		"Spare Part",
		fields=[
			"name",
			"part_name",
			"device_type",
			"stock_qty",
			"reorder_level",
			"unit_cost",
			"selling_price",
		],
	)

	data = []

	for part in parts:
		margin = 0

		if part.unit_cost:
			margin = ((part.selling_price - part.unit_cost) / part.unit_cost) * 100

		total_value = part.stock_qty * part.unit_cost

		data.append(
			{
				"part_name": part.part_name,
				"name": part.name,
				"device_type": part.device_type,
				"stock_qty": part.stock_qty,
				"reorder_level": part.reorder_level,
				"unit_cost": part.unit_cost,
				"selling_price": part.selling_price,
				"margin": margin,
				"total_value": total_value,
			}
		)

	return data


def get_summary(data):
	total_parts = len(data)

	below_reorder = len([d for d in data if d["stock_qty"] <= d["reorder_level"]])

	total_inventory = sum([d["total_value"] for d in data])

	return [
		{"label": _("Total Parts"), "value": total_parts, "indicator": "blue"},
		{"label": _("Below Reorder"), "value": below_reorder, "indicator": "red"},
		{"label": _("Total Inventory Value"), "value": total_inventory, "indicator": "green"},
	]
