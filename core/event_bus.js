const redis = require("redis");

const pub = redis.createClient();
const sub = redis.createClient();

pub.connect();
sub.connect();

function publish(channel, data) {
    pub.publish(channel, JSON.stringify(data));
}

function subscribe(channel, handler) {
    sub.subscribe(channel, (msg) => {
        handler(JSON.parse(msg));
    }, false);
}

module.exports = { publish, subscribe };
