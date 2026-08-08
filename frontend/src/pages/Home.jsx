import { useNavigate } from "react-router-dom";

export default function Home() {
  const nav = useNavigate();

  return (
    <main id="center">
      <section className="hero" style={{ padding: 48 }}>
        <div style={{ maxWidth: 640, textAlign: "left", margin: "0 auto" }}>
          <div style={badgeStyle}>AI-Powered Technical Interviews</div>
          <h2>Intmate — Your AI Interview Agent</h2>
          <p style={{ fontSize: 18, color: "var(--text)", margin: "12px 0 24px" }}>
            Run adaptive, AI-powered technical interviews that assess real-world skills
            from your learning journey and deliver actionable feedback.
          </p>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            <button onClick={() => nav("/setup")} style={primaryButton}>Start Interview</button>
            <button onClick={() => nav("/results")} style={secondaryButton}>View Results</button>
          </div>

          <div id="next-steps" style={{ marginTop: 32 }}>
            <div>
              <h2>How it works</h2>
              <p style={{ color: "var(--text)" }}>
                Select a candidate profile, and the AI interviewer adapts every
                question in real time based on your answers and curriculum progress.
              </p>
            </div>
            <div>
              <h2>Features</h2>
              <ul className="hero-feature-list">
                <li>Adaptive, multi-turn question generation</li>
                <li>Automated per-answer evaluation and feedback</li>
                <li>Human-readable results dashboard</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <div id="spacer" />
    </main>
  );
}

const badgeStyle = {
  display: "inline-block",
  fontSize: 12,
  fontWeight: 600,
  letterSpacing: 0.4,
  color: "var(--accent)",
  background: "var(--accent-bg)",
  border: "1px solid var(--accent-border)",
  padding: "6px 12px",
  borderRadius: 999,
  marginBottom: 12,
};

const primaryButton = {
  padding: "12px 18px",
  borderRadius: 10,
  border: "none",
  background: "linear-gradient(90deg,#4f46e5,#6b46c1)",
  color: "white",
  fontWeight: 600,
};

const secondaryButton = {
  padding: "12px 18px",
  borderRadius: 10,
  border: "1px solid var(--border)",
  background: "transparent",
  color: "var(--text-h)",
};
