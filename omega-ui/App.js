import React, { useEffect, useRef } from "react";

export default function App() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765");
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    let particles = [];

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      particles = data.particles;
    };

    function draw() {
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        const x = p.x * canvas.width;
        const y = p.y * canvas.height;

        const brightness = Math.min(255, p.weight * 255);

        let color = "white";
        if (p.state === "A") color = `rgb(${brightness},50,50)`;
        if (p.state === "B") color = `rgb(50,${brightness},50)`;
        if (p.state === "C") color = `rgb(50,50,${brightness})`;

        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(draw);
    }

    draw();
  }, []);

  return (
    <canvas
      ref={canvasRef}
      width={window.innerWidth}
      height={window.innerHeight}
    />
  );
}
