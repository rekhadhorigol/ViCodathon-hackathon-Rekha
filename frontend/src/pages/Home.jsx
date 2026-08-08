import { useNavigate } from "react-router-dom";

export default function Home() {
  const nav = useNavigate();

  return (
    <main id="center">
      <section className="hero" style={{ padding: 48 }}>
        <div style={{ display: "flex", gap: 36, alignItems: "center", justifyContent: "center" }}>
          <div style={{ maxWidth: 560, textAlign: "left" }}>
            <h1>Vicodathon — AI interview platform</h1>
            <p style={{ fontSize: 18, color: "var(--text)", margin: "12px 0 24px" }}>
              Run adaptive, AI-powered technical interviews that assess real-world skills and deliver actionable feedback.
            </p>

            <div style={{ display: "flex", gap: 12 }}>
              <button onClick={() => nav("/setup")} style={primaryButton}>Start Interview</button>
              <button onClick={() => nav("/results")} style={secondaryButton}>View Results</button>
            </div>

            <div id="next-steps" style={{ marginTop: 32 }}>
              <div>
                <h2>How it works</h2>
                <p style={{ color: "var(--text)" }}>
                  Select a candidate profile, configure the interview, and the AI will adapt questions based on answers and curriculum progress.
                </p>
              </div>
              <div>
                <h2>Features</h2>
                <ul style={{ textAlign: "left", marginTop: 12 }}>
                  <li>Adaptive question generation</li>
                  <li>Automated evaluation and feedback</li>
                  <li>Professional results dashboard</li>
                </ul>
              </div>
            </div>
          </div>

          <div style={{ width: 360, borderRadius: 12, boxShadow: "var(--shadow)", padding: 18, background: "linear-gradient(180deg, rgba(79,70,229,0.06), rgba(170,59,255,0.03))" }}>
            <img src="/src/assets/hero.png" alt="hero" style={{ width: "100%", borderRadius: 8 }} />
          </div>
        </div>
      </section>

      <div id="spacer" />
    </main>
  );
}

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