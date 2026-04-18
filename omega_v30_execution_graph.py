from omega_v29_node_bus import emit

def execute_node(node_name, input_data):
    result = f"{node_name} processed {input_data}"

    emit(node_name, "execution", {
        "input": input_data,
        "output": result
    })

    return result
