# ==================================================
# 🧠 OMEGA VISUAL FIX PATCH (v11 CONTRACT RESTORATION)
# ==================================================

# -------------------------
# ⚠️ GRID SAFETY RULE
# -------------------------
def grid_safe(SIZE, x, y):
    return (
        int(max(0, min(SIZE - 1, x))),
        int(max(0, min(SIZE - 1, y)))
    )


# -------------------------
# 🌊 SAFE TRAIL RENDER
# -------------------------
def render_trail(grid, t):
    x, y = grid_safe(len(grid), t["x"], t["y"])
    grid[y][x] = "✦" if t.get("returning", False) else "●"


# -------------------------
# ⚛️ SAFE PARTICLE RENDER
# -------------------------
def render_particle(grid, p, color_func):
    x, y = grid_safe(len(grid), p.x, p.y)
    grid[y][x] = color_func(p)


# -------------------------
# 🧬 BASE COLOR SYSTEM (v11 RESTORE)
# -------------------------
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def particle_color(p):
    return base_colors[(p.id + int(p.x + p.y)) % len(base_colors)]


# -------------------------
# 🧠 OMEGA VISUAL CONTRACT (LOCKED)
# -------------------------
OMEGA_V11_HEADER = """
==================================================
🧠 OMEGA v11 — STABILIZED EVENT FIELD
==================================================
📦 Files
🐍 Python
🔗 Node Files
🟣 Particles
⚡ Jumps
🌈 Returns / Trails
📡 Events
==================================================
"""


# -------------------------
# 📊 FOOTER RENDER (ALWAYS APPENDED)
# -------------------------
def render_footer(total, py, node, particles, jumps, trails, events):
    print(OMEGA_V11_HEADER)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("--------------------------------------------------")
    print(f"🟣 Particles    : {particles}")
    print(f"⚡ Total Jumps  : {jumps}")
    print(f"🌈 Trails       : {trails}")
    print(f"📡 Events       : {events}")
    print("==================================================")

    print("\nKEY:")
    print("🟣🟢🔵⚪ = particle state")
    print("● = quantum return trail")
    print("✦ = signal event")
    print("🟩🟨🟧🟥🔥 = intensity")
