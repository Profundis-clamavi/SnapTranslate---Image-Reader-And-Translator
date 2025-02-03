const express = require("express");
const path = require("path");
const livereload = require("livereload");
const connectLivereload = require("connect-livereload");

const app = express();
const PORT = 1234;

// Live reload setup
const liveReloadServer = livereload.createServer();
liveReloadServer.watch(path.join(__dirname, "public"));
app.use(connectLivereload());

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

liveReloadServer.server.once("connection", () => {
  setTimeout(() => {
    liveReloadServer.refresh("/");
  }, 100);
});
