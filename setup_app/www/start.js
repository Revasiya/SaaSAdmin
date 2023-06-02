const { createApp } = Vue;
if (window.dev_server) {
  domain = ".localhost:8000";
} else {
  domain = ".onehash.store";
}
frappe.ready(() => {
  console.log("ready");
  frappe.socketio.init();
});

createApp({
  data() {
    return {
      fname: "",
      lname: "",
      email: "",
      password: "",
      siteCreated: false,
      loading: false,
      sitename: "",
      comapany_name: "",
      inputErrors: [],
      targetSubdomain: "",
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
    checkSiteCreated() {
      console.log("checking site created");
      let response;
      frappe.call({
        method:
          "setup_app.setup_app.doctype.saas_sites.saas_sites.checkSiteCreated",
        args: {
          doc: {
            domain: this.sitename,
          },
        },
        async: false,
        callback: (r) => {
          console.log("output", r.message);
          if (r.message == "yes") {
            this.siteCreated = true;
          }
          response = r.message;
        },
      });
      return response;
    },
    checkSiteCreatedPoll() {
      console.log("polling site creation");
      this.checkSiteCreated();
      if (this.siteCreated) {
        this.status.step3 = "completed";
        const pass = this.password.replaceAll(/#/g, "%23");
        const query = `?domain=${this.sitename}&email=${this.email}&password=${pass}&firstname=${this.fname}&lastname=${this.lname}&companyname=${this.comapany_name}`;
        setTimeout(() => {
          let domainToRedirect = "";
          if (window.dev_server) {
            domainToRedirect = this.targetSubdomain;
          } else {
            domainToRedirect = this.sitename;
          }
          window.location.href =
            `http://${domainToRedirect}${domain}/redirect` + query;
        }, 2000);
      } else {
        setTimeout(() => {
          this.checkSiteCreatedPoll();
        }, 3000);
      }
    },
    createSite() {
      this.loading = true;
      this.status.step1 = "active";
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
            this.targetSubdomain = r.message;
            console.log("message", r.message);
            this.checkSiteCreatedPoll();
          }
        },
      });
    },
  },
}).mount("#apsp");
