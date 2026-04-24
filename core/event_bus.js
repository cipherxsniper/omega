const events = {};

function on(event, fn) {
  if (!events[event]) events[event] = [];
  events[event].push(fn);
}

function emit(event, data) {
  if (!events[event]) return;
  events[event].forEach(fn => fn(data));
}

module.exports = { on, emit };
