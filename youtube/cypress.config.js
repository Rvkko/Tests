const { defineConfig } = require("cypress");

module.exports = defineConfig({
  env: {
    email: "testacctmanager24@gmail.com",
    password: "Admin123!",
  },

  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
