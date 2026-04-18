def pressure(node):
    mem=len(node.get("mem",[]))/100
    stab=1-node.get("stability",0.5)
    inf=1-node.get("influence",0.5)
    return min(1,max(0, mem*0.4 + stab*0.4 + inf*0.2))

def state(p):
    if p>0.75: return "SPLIT"
    if p>0.5: return "ADAPT"
    if p>0.25: return "LEARN"
    return "STABLE"
