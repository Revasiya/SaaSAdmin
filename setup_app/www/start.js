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
      inputErrors: [],
    };
  },
  mounted() {
    inputClasses = document.querySelectorAll(".input");
    console.log(inputClasses);
    inputClasses.forEach((input) => {
      document.getElementById(input.id).addEventListener("focus", () => {
        console.log("focus");
        input.classList.remove("error");
      });
      document.getElementById(input.id).addEventListener("onchange", () => {
        console.log("change");
      });
    });
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
    validateInput(fname, lname, email, password, sitename, comapany_name) {
      this.inputErrors = [];
      let isOk = true;
      if (!fname) {
        this.inputErrors.push("First Name is required");
        document.getElementById("firstname").classList.add("error");
        isOk = false;
      }
      if (!lname) {
        this.inputErrors.push("Last Name is required");
        document.getElementById("lastname").classList.add("error");
        isOk = false;
      }
      if (!email) {
        this.inputErrors.push("Email is required");
        document.getElementById("email").classList.add("error");
        isOk = false;
      }
      if (!password) {
        this.inputErrors.push("Password is required");
        document.getElementById("password").classList.add("error");
        isOk = false;
      }
      if (!sitename) {
        this.inputErrors.push("Site Name is required");
        document.getElementById("sitename").classList.add("error");
        isOk = false;
      }
      if (!comapany_name) {
        this.inputErrors.push("Company Name is required");
        document.getElementById("companyname").classList.add("error");
        isOk = false;
      }
      return isOk;
    },
    createSite() {
      console.log(
        "crete site",
        this.fname,
        this.lname,
        this.email,
        this.password,
        this.sitename,
        this.comapany_name
      );
      if (
        !this.validateInput(
          this.fname,
          this.lname,
          this.email,
          this.password,
          this.sitename,
          this.comapany_name
        )
      ) {
        return;
      }
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
            console.log(r.message);
          }
        },
      });
    },
  },
}).mount("#apsp");
