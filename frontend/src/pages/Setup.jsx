import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateSessionId } from "../utils/session";
import candidatesData from "../data/candidates.json";

// Local candidate data (matching backend candidate IDs) — no endpoint needed, it's static.
const candidates = candidatesData.candidates || [];

export default function Setup() {
  const nav = useNavigate();
  const [candidateId, setCandidateId] = useState("");
  const [loading, setLoading] = useState(false);

  const selected = candidates.find((c) => c.member.id === candidateId);
  const completedCount = selected?.missions?.filter((m) => m.passed).length ?? 0;

  function start() {
    if (!candidateId) return alert("Please select a candidate.");
    setLoading(true);
    const sessionId = generateSessionId();
    // Save session to localStorage for the interview flow.
    localStorage.setItem("intmate.sessionId", sessionId);
    localStorage.setItem("intmate.candidateId", candidateId);

    setTimeout(() => {
      setLoading(false);
      nav("/interview");
    }, 400);
  }

  return (
    <div className="page">
      <h2>Interview Setup</h2>
      <p style={{ color: "var(--text)" }}>Choose a candidate to begin their AI-adapted technical interview.</p>

      <div className="two-col">
        <div>
          <label style={{ display: "block", marginBottom: 8 }}>Candidate</label>
          <select value={candidateId} onChange={(e) => setCandidateId(e.target.value)} style={selectStyle}>
            <option value="">Select a candidate</option>
            {candidates.map((c) => (
              <option key={c.member.id} value={c.member.id}>{`${c.member.name} — ${c.member.jobRole}`}</option>
            ))}
          </select>

          <div style={{ marginTop: 24 }}>
            <button onClick={() => window.history.back()} style={{ marginRight: 8 }}>Back</button>
            <button onClick={start} style={primaryButton} disabled={loading}>{loading ? "Starting..." : "Start Interview"}</button>
          </div>
        </div>

        <aside className="card">
          <h3 style={{ marginTop: 0 }}>Preview</h3>
          {selected ? (
            <>
              <p style={{ color: "var(--text)" }}>Candidate: <strong style={{ color: "var(--text-h)" }}>{selected.member.name}</strong></p>
              <p style={{ color: "var(--text)" }}>Role: <strong style={{ color: "var(--text-h)" }}>{selected.member.jobRole}</strong></p>
              <p style={{ color: "var(--text)" }}>Experience: <strong style={{ color: "var(--text-h)" }}>{selected.member.yearsExperience} years</strong></p>
              <p style={{ color: "var(--text)" }}>Completed missions: <strong style={{ color: "var(--text-h)" }}>{completedCount}</strong></p>
            </>
          ) : (
            <p style={{ color: "var(--text)" }}>Select a candidate to see their profile here.</p>
          )}
          <div style={{ height: 12 }} />
          <p style={{ color: "var(--text)", fontSize: 13 }}>
            The interview questions and feedback are generated live by the AI and adapt to the candidate's answers as they go.
          </p>
        </aside>
      </div>
    </div>
  );
}

const selectStyle = { width: "100%", padding: 10, borderRadius: 8, border: "1px solid var(--border)", background: "var(--bg)", color: "var(--text-h)" };
const primaryButton = { padding: "10px 16px", borderRadius: 8, background: "linear-gradient(90deg,#4f46e5,#6b46c1)", color: "white", border: "none" };
