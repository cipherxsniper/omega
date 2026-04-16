from system.omega_contract_v10 import OmegaContractV10

def safe_step(recursive_engine):
    raw = recursive_engine.step()
    return OmegaContractV10.normalize(raw)

def get_strongest(rec):
    rec = OmegaContractV10.normalize(rec)
    return rec["strongest"]
