from omega.core.self_evolving_kernel_v8 import EvolutionKernelV8

KERNEL = EvolutionKernelV8()

def propose_fix(node_name, file_path, patch_text, reason=""):
    return KERNEL.propose_mutation(
        node_name=node_name,
        mutation_type="contract_patch",
        payload={
            "file": file_path,
            "patch": patch_text,
            "reason": reason
        }
    )
