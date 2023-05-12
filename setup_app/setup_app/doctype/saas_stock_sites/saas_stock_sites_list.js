function refresh() {
  frappe
    .call(
      "setup_app.setup_app.doctype.saas_stock_sites.saas_stock_sites.refreshStockSites"
    )
    .then((r) => {
      frappe.msgprint(__("Sites refreshed"));
    });
}

frappe.listview_settings["SaaS stock sites"] = {
  onload(listview) {
    listview.page.set_secondary_action(
      "Refresh sites",
      () => refresh(),
      "octicon octicon-sync"
    );
  },
};
