from file_scanner import scan_files
from dag_validator import build_dependency_graph, validate_graph
from stability_engine import compute_stability
from repair_planner import generate_repair_plan
from task_queue import TaskQueue

def main():
    print("🧠 OMEGA SIGNAL ENGINE v2 STARTED")

    files = scan_files(".")

    graph = build_dependency_graph(files)
    issues = validate_graph(graph)

    stability = compute_stability(graph, issues)

    planner = generate_repair_plan(graph, issues, stability)

    queue = TaskQueue()
    queue.load(planner)

    print("\n📊 SYSTEM REPORT")
    print("Stability:", stability["global_score"])
    print("Issues:", len(issues))
    print("Queued Tasks:", queue.size())

    print("\n🧠 READY (NO AUTO EXECUTION MODE)")

if __name__ == "__main__":
    main()
