from runtime_v7.core.v83_execution_engine import SwarmExecutionEngineV83


def attach_execution_engine(node):
    node.engine = SwarmExecutionEngineV83(node)
    node.engine.start()

    return node.engine
