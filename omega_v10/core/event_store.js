const fs = require("fs");

class EventStore {
  constructor() {
    this.logFile = "omega_v10_stream.log";
  }

  append(event) {
    fs.appendFileSync(this.logFile, JSON.stringify(event) + "\n");
  }
}

module.exports = EventStore;
