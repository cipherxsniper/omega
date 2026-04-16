const { createClient } = require("redis");

class RedisMesh {
  constructor() {
    this.pub = createClient();
    this.sub = this.pub.duplicate();
  }

  async connect() {
    await this.pub.connect();
    await this.sub.connect();
  }

  async emit(channel, data) {
    await this.pub.publish(channel, JSON.stringify(data));
  }

  async listen(channel, cb) {
    await this.sub.subscribe(channel, (msg) => {
      cb(JSON.parse(msg));
    });
  }
}

module.exports = RedisMesh;
