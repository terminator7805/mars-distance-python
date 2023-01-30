window.addEventListener("DOMContentLoaded", () => {
  var python = require("child_process").spawn("python", ["./python/main.py"]);
});
