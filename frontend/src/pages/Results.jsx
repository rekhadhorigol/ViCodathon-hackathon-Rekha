import { useEffect, useState } from "react";
import api from "../services/api";

export default function Results() {
  const [sessionId] = useState(localStorage.getItem("vicodathon.sessionId") || "");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!sessionId) return;
    setLoading(true);
    api.getResult(sessionId)
      .then((r) => setResult(r))
      .catch((e) => setError(e.message || "Failed to load results."))
      .finally(() => setLoading(false));
  }, [sessionId]);

  if (!sessionId) return <div style={{ padding: 28 }}>No session found. Start an interview first.</div>;

  return (
    <div style={{ padding: 28 }}>
      <h2>Results</h2>
      {loading && <div>Loading evaluation...</div>}
      {error && <div style={{ color: "#b91c1c" }}>{error}</div>}
      {result && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20 }}>
          <div>
            <div style={{ padding: 18, borderRadius: 10, background: "white", boxShadow: "var(--shadow)" }}>
              <h3>Overall</h3>
              <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(result.overallEvaluation, null, 2)}</pre>
            </div>

            <div style={{ marginTop: 16 }}>
              <h3>Question evaluations</h3>
              {result.evaluations.map((ev) => (
                <div key={ev.questionNumber} style={{ padding: 12, borderRadius: 8, background: "var(--code-bg)", marginBottom: 8 }}>
                  <div style={{ fontWeight: 600 }}>Q{ev.questionNumber}: {ev.question}</div>
                  <div style={{ marginTop: 6 }}>{ev.evaluation?.feedback || "No evaluation"}</div>
                </div>
              ))}
            </div>
          </div>

          <aside style={{ borderRadius: 12, padding: 18, background: "var(--code-bg)", boxShadow: "var(--shadow)" }}>
            <h3>Session</h3>
            <p>Session ID: <code className="counter">{sessionId}</code></p>
            <div style={{ height: 12 }} />
            <button onClick={() => { localStorage.removeItem("vicodathon.sessionId"); localStorage.removeItem("vicodathon.candidateId"); location.href = "/"; }}>Start New Interview</button>
          </aside>
        </div>
      )}
    </div>
  );
}
