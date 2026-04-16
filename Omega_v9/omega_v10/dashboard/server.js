const express = require("express");
const http = require("http");
const socket = require("socket.io");
const fs = require("fs");

const app = express();
const server = http.createServer(app);
const io = socket(server);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

setInterval(() => {
  try {
    const lines = fs.readFileSync("../core/omega_v10_stream.log", "utf8")
      .trim().split("\n").slice(-20);

    io.emit("stream", lines);
  } catch (e) {}
}, 500);

server.listen(3000, () => {
  console.log("🧠 Omega Dashboard running on http://localhost:3000");
});
