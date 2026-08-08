import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const VERDICT_COLORS = {
  WEAK: "#b91c1c",
  DEVELOPING: "#b45309",
  STRONG: "#15803d",
  EXCELLENT: "#4f46e5",
};

function VerdictBadge({ verdict }) {
  if (!verdict) return null;
  const color = VERDICT_COLORS[verdict] || "var(--text)";
  return (
    <span style={{
      display: "inline-block",
      padding: "4px 10px",
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 700,
      color: "white",
      background: color,
    }}>
      {verdict}
    </span>
  );
}

function ScoreDial({ score }) {
  if (score == null) return null;
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 4 }}>
      <span style={{ fontSize: 32, fontWeight: 700, color: "var(--text-h)" }}>{score}</span>
      <span style={{ fontSize: 14, color: "var(--text)" }}>/ 10</span>
    </div>
  );
}

function BulletList({ items, emptyLabel }) {
  if (!items || items.length === 0) {
    return <p style={{ color: "var(--text)", fontSize: 13 }}>{emptyLabel}</p>;
  }
  return (
    <ul style={{ margin: "8px 0 0", paddingLeft: 18 }}>
      {items.map((item, i) => (
        <li key={i} style={{ color: "var(--text)", marginBottom: 4 }}>{item}</li>
      ))}
    </ul>
  );
}

export default function Results() {
  const nav = useNavigate();
  const [sessionId] = useState(localStorage.getItem("intmate.sessionId") || "");
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

  function startNew() {
    localStorage.removeItem("intmate.sessionId");
    localStorage.removeItem("intmate.candidateId");
    nav("/setup");
  }

  if (!sessionId) return <div className="page">No session found. Start an interview first.</div>;

  const overall = result?.overallEvaluation;

  return (
    <div className="page">
      <h2>Results</h2>
      {loading && <div>Loading evaluation...</div>}
      {error && <div style={{ color: "#b91c1c" }}>{error}</div>}
      {result && (
        <div className="two-col">
          <div>
            <div className="card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 16, flexWrap: "wrap" }}>
                <div>
                  <h3 style={{ marginTop: 0, marginBottom: 6 }}>Overall Assessment</h3>
                  <VerdictBadge verdict={overall?.verdict} />
                </div>
                <ScoreDial score={overall?.overallScore} />
              </div>

              <p style={{ color: "var(--text-h)", marginTop: 16 }}>
                {overall?.technicalStrength || "No summary available."}
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 16 }}>
                <div>
                  <h4 style={{ margin: "0 0 4px" }}>Strongest areas</h4>
                  <BulletList items={overall?.strongestAreas} emptyLabel="None recorded." />
                </div>
                <div>
                  <h4 style={{ margin: "0 0 4px" }}>Areas to improve</h4>
                  <BulletList items={overall?.areasToImprove} emptyLabel="None recorded." />
                </div>
              </div>

              {overall?.technicalGaps?.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <h4 style={{ margin: "0 0 4px" }}>Technical gaps</h4>
                  <BulletList items={overall?.technicalGaps} emptyLabel="" />
                </div>
              )}

              {overall?.recommendation && (
                <div style={{ marginTop: 16, padding: 12, borderRadius: 8, background: "var(--code-bg)" }}>
                  <strong style={{ color: "var(--text-h)" }}>Recommendation: </strong>
                  <span style={{ color: "var(--text)" }}>{overall.recommendation}</span>
                </div>
              )}
            </div>

            <div style={{ marginTop: 16 }}>
              <h3>Question-by-question evaluation</h3>
              {result.evaluations.map((ev) => (
                <div key={ev.questionNumber} className="card" style={{ marginBottom: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, flexWrap: "wrap" }}>
                    <div style={{ fontWeight: 600, color: "var(--text-h)" }}>Q{ev.questionNumber}: {ev.question}</div>
                    <VerdictBadge verdict={ev.evaluation?.verdict} />
                  </div>
                  <div style={{ marginTop: 8, color: "var(--text)" }}>{ev.evaluation?.feedback || "No evaluation"}</div>
                  {ev.evaluation?.strengths?.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <strong style={{ fontSize: 13, color: "var(--text-h)" }}>Strengths: </strong>
                      <span style={{ fontSize: 13, color: "var(--text)" }}>{ev.evaluation.strengths.join(", ")}</span>
                    </div>
                  )}
                  {ev.evaluation?.improvements?.length > 0 && (
                    <div style={{ marginTop: 4 }}>
                      <strong style={{ fontSize: 13, color: "var(--text-h)" }}>Improvements: </strong>
                      <span style={{ fontSize: 13, color: "var(--text)" }}>{ev.evaluation.improvements.join(", ")}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          <aside className="card">
            <h3 style={{ marginTop: 0 }}>Session</h3>
            <p>Session ID: <code className="counter">{sessionId}</code></p>
            <div style={{ height: 12 }} />
            <button onClick={startNew} style={primaryButton}>Start New Interview</button>
          </aside>
        </div>
      )}
    </div>
  );
}

const primaryButton = { padding: "10px 16px", borderRadius: 8, background: "linear-gradient(90deg,#4f46e5,#6b46c1)", color: "white", border: "none", width: "100%" };
