from omega_v31_edit_proposals import propose_edit
from omega_v31_patch_applier import apply_proposal

def generate_reply(intent, message, history):

    if "modify" in message:
        proposal = propose_edit(
            "user",
            "app.py",
            message,
            "user requested modification"
        )

        return str(proposal)

    if "apply" in message:
        return apply_proposal({
            "id": 1,
            "target": "app.py",
            "change": message
        })

    return "🧠 Omega v31: Governance layer active. Awaiting structured input."
