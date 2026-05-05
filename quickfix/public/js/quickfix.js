frappe.ready(() => {
	if (frappe.boot.quickfix_shop_name) {
		console.log("Shop:", frappe.boot.quickfix_shop_name);
	}
});
