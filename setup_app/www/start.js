const { createApp } = Vue;
let domain = "onehash.store";
if (window.dev_server) {
  frappe.boot.socketio_port = "9001"; //use socketio port shown when bench starts
  domain = "localhost";
}
frappe.ready(() => {
  console.log("ready");
  frappe.socketio.init();
});
console.log(frappe.socketio);

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

    frappe.socketio.socket.on("site_created", (data) => {
      if (window.dev_server) {
        window.location.href = `http://${data.site}.${domain}:8000`;
      } else {
        window.location.href = `https://${data.site}.${domain}`;
      }
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
