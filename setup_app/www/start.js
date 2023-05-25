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
      loading: false,
      sitename: "",
      comapany_name: "",
      inputErrors: [],
      status: {
        step1: "neutral",
        step2: "neutral",
        step3: "neutral",
      },
    };
  },

  mounted() {
    inputClasses = document.querySelectorAll(".input");
    console.log(inputClasses);
    inputClasses.forEach((input) => {
      document.getElementById(input.id).addEventListener("focus", () => {
        input.classList.remove("uk-form-danger");
      });
      document.getElementById(input.id).addEventListener("onchange", () => {
        console.log("change");
      });
    });
  },
  created() {
    frappe.socketio.init();

    frappe.socketio.socket.on("site_created", (data) => {
      console.log("site created");
      this.status.step3 = "completed";
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
      const errorClass = "uk-form-danger";
      let isOk = true;
      if (!fname) {
        this.inputErrors.push("First Name is required");
        document.getElementById("firstname").classList.add(errorClass);
        isOk = false;
      }
      if (!lname) {
        this.inputErrors.push("Last Name is required");
        document.getElementById("lastname").classList.add(errorClass);
        isOk = false;
      }
      if (!email) {
        this.inputErrors.push("Email is required");
        document.getElementById("email").classList.add(errorClass);
        isOk = false;
      }
      if (!password) {
        this.inputErrors.push("Password is required");
        document.getElementById("password").classList.add(errorClass);
        isOk = false;
      }
      if (!sitename) {
        this.inputErrors.push("Site Name is required");
        document.getElementById("sitename").classList.add(errorClass);
        isOk = false;
      }
      if (!comapany_name) {
        this.inputErrors.push("Company Name is required");
        document.getElementById("companyname").classList.add(errorClass);
        isOk = false;
      }
      return isOk;
    },
    createSite() {
      this.loading = true;
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
        this.loading = false;
        return;
      }
      this.status.step1 = "loading";

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
        callback: (r) => {
          console.log("functon called", r);
          this.status.step1 = "completed";
          this.status.step2 = "completed";
          if (r.message) {
            console.log(r.message);
          }
        },
      });
    },
  },
}).mount("#apsp");
