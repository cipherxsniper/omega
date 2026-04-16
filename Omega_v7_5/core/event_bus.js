const EventEmitter = require("events");

class OmegaEventBus extends EventEmitter {
  constructor() {
    super();
    this.queue = [];
  }

  emitEvent(event) {
    event.timestamp = Date.now();
    this.queue.push(event);
    this.emit("event", event);
  }

  batch(size = 5) {
    const batch = this.queue.splice(0, size);
    return batch;
  }
}

module.exports = new OmegaEventBus();
