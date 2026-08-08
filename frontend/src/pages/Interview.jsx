import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import candidatesData from "../data/candidates.json";

const TOTAL_QUESTIONS = 8; // must match MAX_QUESTIONS in the backend interview service

export default function Interview() {
  const nav = useNavigate();
  const [sessionId] = useState(localStorage.getItem("intmate.sessionId") || "");
  const [candidateId] = useState(localStorage.getItem("intmate.candidateId") || "");
  const [question, setQuestion] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const hasStartedRef = useRef(false);

  const candidateName =
    candidatesData.candidates?.find((c) => c.member.id === candidateId)?.member?.name || candidateId;

  useEffect(() => {
    if (!sessionId || !candidateId) {
      nav("/setup");
      return;
    }

    if (hasStartedRef.current) {
      return;
    }

    hasStartedRef.current = true;
    fetchNext();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId, candidateId, nav]);

  async function fetchNext(latestAnswer = null) {
    setLoading(true);
    setError("");
    try {
      const payload = { sessionId, candidateId, answer: latestAnswer };
      const res = await api.startInterview(payload);
      if (res.question) {
        setQuestion(res.question);
        setQuestionNumber(res.questionNumber || 0);
      } else if (res.completed) {
        try {
          await api.evaluateOverall({
            sessionId,
            candidateId,
            questionNumber,
            answer: latestAnswer || answer,
          });
          nav("/results");
        } catch (overallError) {
          setError(overallError.message || "Failed to complete the final evaluation.");
        }
      }
    } catch (e) {
      setError(e.message || "Failed to fetch question.");
    } finally {
      setLoading(false);
    }
  }

  async function submit() {
    if (!answer.trim()) return alert("Please enter an answer.");
    setLoading(true);
    try {
      await api.evaluate({ sessionId, candidateId, questionNumber, answer });
      setAnswer("");
      await fetchNext(answer);
    } catch (e) {
      setError(e.message || "Failed to submit answer.");
    } finally {
      setLoading(false);
    }
  }

  function exitInterview() {
    if (!confirm("Ending now will discard this interview without generating results. Continue?")) return;
    localStorage.removeItem("intmate.sessionId");
    localStorage.removeItem("intmate.candidateId");
    nav("/setup");
  }

  const progressPct = Math.min(100, Math.round((questionNumber / TOTAL_QUESTIONS) * 100));

  return (
    <div className="page">
      <h2>Interview</h2>
      {error && <div style={{ color: "#b91c1c" }}>{error}</div>}

      <div className="two-col">
        <div>
          <div className="card">
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8, alignItems: "baseline" }}>
              <div>Question {questionNumber || "—"} of {TOTAL_QUESTIONS}</div>
              <div style={{ fontSize: 13, color: "var(--text)" }}>{progressPct}% complete</div>
            </div>

            <div className="progress-track" style={{ marginBottom: 16 }}>
              <div className="progress-fill" style={{ width: `${progressPct}%` }} />
            </div>

            <div style={{ minHeight: 140, padding: 12, borderRadius: 8, background: "var(--code-bg)", color: "var(--text-h)" }}>
              {loading ? "Loading question..." : question || "No question yet."}
            </div>

            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Write your answer here..."
              style={{ width: "100%", minHeight: 120, marginTop: 12, padding: 12, borderRadius: 8, border: "1px solid var(--border)", background: "var(--bg)", color: "var(--text-h)", boxSizing: "border-box" }}
            />

            <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
              <button onClick={exitInterview}>Exit</button>
              <button onClick={submit} style={{ background: "linear-gradient(90deg,#4f46e5,#6b46c1)", color: "white", border: "none", padding: "10px 14px", borderRadius: 8 }} disabled={loading}>{loading ? "Submitting..." : "Submit Answer"}</button>
            </div>
          </div>
        </div>

        <aside className="card">
          <h3 style={{ marginTop: 0 }}>Session</h3>
          <p>Session ID: <code className="counter">{sessionId || "—"}</code></p>
          <p>Candidate: <strong style={{ color: "var(--text-h)" }}>{candidateName || "—"}</strong></p>
          <div style={{ height: 12 }} />
          <p style={{ color: "var(--text)", fontSize: 13 }}>
            Exiting early discards this interview since final results require all {TOTAL_QUESTIONS} questions to be answered.
          </p>
        </aside>
      </div>
    </div>
  );
}
