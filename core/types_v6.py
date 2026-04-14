def create_entity(entity_id):
    return {
        "id": entity_id,
        "trust": 0.5,
        "wealth": 100.0,
        "compute": 1.0,
        "status": "active"
    }


def create_law(law_id, name):
    return {
        "id": law_id,
        "name": name,
        "code": "",
        "intent": "",
        "authority_weight": 1.0,
        "vote_score": 0.5,
        "status": "active",
        "version": 1,
        "created_by": "system",
        "last_modified": 0.0
    }
