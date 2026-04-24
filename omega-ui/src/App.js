import React, { useState, useEffect } from "react";

export default function App() {
  const [cmd, setCmd] = useState("");
  const [log, setLog] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [brain, setBrain] = useState({ nodes: [] });

  const run = async () => {
    const res = await fetch("http://localhost:3001/cmd", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ command: cmd })
    });

    const data = await res.json();

    setLog(prev => [...prev, "~Omega€ " + cmd, JSON.stringify(data.output)]);

    setCmd("");
  };

  const predict = async (value) => {
    setCmd(value);

    const res = await fetch("http://localhost:3001/cmd", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ command: "/predict " + value })
    });

    const data = await res.json();
    setPredictions(data.output || []);
  };

  const loadBrain = async () => {
    const res = await fetch("http://localhost:3001/cmd", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ command: "/brain" })
    });

    const data = await res.json();
    setBrain(data.output);
  };

  useEffect(() => {
    const t = setInterval(loadBrain, 2000);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={styles}>

      {/* TERMINAL */}
      <div style={box}>
        <h3>💻 ~Omega€ Predictive Terminal</h3>

        <input
          value={cmd}
          onChange={e=>predict(e.target.value)}
          onKeyDown={e=>e.key==="Enter"&&run()}
          style={input}
        />

        {/* PREDICTIONS */}
        <div>
          {predictions.map((p,i)=>(
            <div key={i} onClick={()=>setCmd(p)}>
              ⚡ {p}
            </div>
          ))}
        </div>
      </div>

      {/* NEURAL BRAIN VISUAL */}
      <div style={box}>
        <h3>🧠 Neural Particle Brain</h3>

        <div style={grid}>
          {brain.nodes?.map((n,i)=>(
            <div key={i}
              style={{
                ...node,
                opacity: n.heat || 0.2,
                transform:`scale(${1 + (n.weight*0.1)})`
              }}>
              {n.id}
            </div>
          ))}
        </div>
      </div>

      {/* LOG */}
      <div style={box}>
        {log.map((l,i)=><div key={i}>{l}</div>)}
      </div>

    </div>
  );
}

const styles = {
  background:"#000",
  color:"#00ffcc",
  fontFamily:"monospace",
  height:"100vh",
  overflow:"auto"
};

const box = {
  border:"1px solid #00ffcc",
  margin:10,
  padding:10
};

const input = {
  width:"100%",
  background:"#000",
  color:"#00ffcc"
};

const grid = {
  display:"flex",
  flexWrap:"wrap",
  gap:10
};

const node = {
  border:"1px solid #00ffcc",
  padding:5,
  fontSize:10
};
