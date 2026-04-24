import React, { useState } from "react";

export default function OmegaShell() {
  const [cmd, setCmd] = useState("");
  const [log, setLog] = useState([]);
  const [mode, setMode] = useState("shell");
  const [aiChat, setAiChat] = useState([]);

  const send = async () => {
    const res = await fetch("http://localhost:3001/cmd", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ command: cmd })
    });

    const data = await res.json();

    setLog(l => [...l, "~Omega€ " + cmd, JSON.stringify(data.output)]);
    setCmd("");
  };

  return (
    <div style={styles}>

      {/* HEADER */}
      <div style={box}>
        <h2>🧠 ~Omega€ Terminal</h2>

        <button onClick={()=>setMode("shell")}>Shell</button>
        <button onClick={()=>setMode("ai")}>AI Assistant</button>
        <button onClick={()=>setMode("brain")}>Brain</button>
      </div>

      {/* SHELL MODE */}
      {mode === "shell" && (
        <div style={box}>
          <input
            value={cmd}
            onChange={e=>setCmd(e.target.value)}
            onKeyDown={e=>e.key==="Enter"&&send()}
            style={input}
          />

          <div>
            {log.map((l,i)=><div key={i}>{l}</div>)}
          </div>
        </div>
      )}

      {/* AI MODE */}
      {mode === "ai" && (
        <div style={box}>
          <h3>🧠 Omega Open AI Assistant</h3>
          <p>Chat with system brain (local intelligence layer)</p>

          <textarea
            style={input}
            onChange={e=>setCmd(e.target.value)}
            value={cmd}
          />

          <button onClick={send}>Ask Omega</button>
        </div>
      )}

      {/* BRAIN MODE */}
      {mode === "brain" && (
        <div style={box}>
          <h3>⚡ Cognitive System View</h3>
          <p>Scripts + execution network visualization</p>
        </div>
      )}

    </div>
  );
}

const styles = {
  background:"#000",
  color:"#00ffcc",
  height:"100vh",
  fontFamily:"monospace"
};

const box = {
  border:"1px solid #00ffcc",
  margin:10,
  padding:10
};

const input = {
  width:"100%",
  background:"#000",
  color:"#00ffcc",
  border:"1px solid #00ffcc"
};
