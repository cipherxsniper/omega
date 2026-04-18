from flask import Flask, request, jsonify
from memory_core import memory

app = Flask(__name__)

def safe_reply(message):
    return f"🧠 Omega: I processed '{message}' with stable cognition layer."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"reply": "⚠️ invalid request"}), 400

        user = data.get("user_id", "unknown")
        msg = data.get("message", "")

        reply = safe_reply(msg)

        memory.add(user, msg, reply)

        return jsonify({
            "reply": reply,
            "memory": memory.summarize()
        })

    except Exception as e:
        print("CRASH RECOVERED:", e)
        return jsonify({"reply": "🧠 Omega self-recovered from error"}), 200


@app.route("/", methods=["GET"])
def home():
    return "🧠 Omega v12 Stable Brain Online"

if __name__ == "__main__":
    print("🧠 OMEGA v12 CORE ONLINE")
    app.run(host="0.0.0.0", port=5000, debug=False)
