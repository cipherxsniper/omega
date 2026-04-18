from omega_language_core_v24 import speak
from omega_wink_runtime_fix_v1 import analyze_system

def run_observer(context="wink_wink"):
    metrics = analyze_system()
    return speak(metrics, context)
