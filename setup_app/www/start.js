const { createApp } = Vue;
if (window.dev_server) {
  frappe.boot.socketio_port = "9001"; //use socketio port shown when bench starts
}
frappe.ready(() => {
  console.log("ready");
  frappe.socketio.init();
  console.log(frappe.socketio.socket.io);
  frappe.socketio.socket.io.on("site_created", (data) => {
    console.log(data, 3);
    window.location = this.subdomain + "." + domain;
  });
  frappe.socketio.socket.io.on("sex", (data) => {
    console.log(data, 3);
    window.location = this.subdomain + "." + domain;
  });
});
console.log(frappe.socketio);

const domain = "onehash.store";
createApp({
  data() {
    return {
      fname: "",
      lname: "",
      email: "",
      password: "",
      sitename: "",
      comapany_name: "",
    };
  },
  created() {
    frappe.socketio.init();
    frappe.socketio.socket.on("connection", () => {
      console.log("eqfd", 3);
    });
    setTimeout(() => {
      console.log(frappe.socketio.socket);
    }, 5000);
  },
  methods: {
    createSite() {
      console.log(window.frappe);
      console.log("creating");
      console.log(
        1,
        this.fname,
        this.lname,
        this.email,
        this.password,
        this.sitename,
        this.comapany_name
      );
      // return;
      // Create a new site
      frappe.call({
        method: "setup_app.setup_app.doctype.saas_sites.saas_sites.test_site",
        args: {
          args: this.comapany_name,
        },
        callback: function (r) {
          console.log(r);
          if (r.message) {
            console.log("done");
          }
        },
      });
      return;
      frappe.call({
        method: "setup_app.setup_app.doctype.saas_sites.saas_sites.setupSite",
        args: {
          doc: {
            company_name: this.comapany_name,
            domain: this.sitename,
            password: this.password,
            email: this.email,
            first_name: this.fname,
            last_name: this.lname,
          },
        },
        callback: function (r) {
          if (r.message) {
            frappe.msgprint(__("Site Created"));
          }
        },
      });
    },
  },
}).mount("#apsp");
