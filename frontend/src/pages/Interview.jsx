import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Interview() {
  const nav = useNavigate();
  const [sessionId] = useState(localStorage.getItem("vicodathon.sessionId") || "");
  const [candidateId] = useState(localStorage.getItem("vicodathon.candidateId") || "");
  const [question, setQuestion] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const hasStartedRef = useRef(false);

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

  return (
    <div style={{ padding: 28 }}>
      <h2>Interview</h2>
      {error && <div style={{ color: "#b91c1c" }}>{error}</div>}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20, marginTop: 18 }}>
        <div>
          <div style={{ padding: 18, borderRadius: 10, background: "white", boxShadow: "var(--shadow)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <div>Question {questionNumber}</div>
              <div>{/* progress */}</div>
            </div>

            <div style={{ minHeight: 140, padding: 12, borderRadius: 8, background: "var(--code-bg)", color: "var(--text-h)" }}>
              {loading ? "Loading question..." : question || "No question yet."}
            </div>

            <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Write your answer here..." style={{ width: "100%", minHeight: 120, marginTop: 12, padding: 12, borderRadius: 8 }} />

            <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
              <button onClick={() => nav("/setup")}>Back</button>
              <button onClick={submit} style={{ background: "linear-gradient(90deg,#4f46e5,#6b46c1)", color: "white", border: "none", padding: "10px 14px", borderRadius: 8 }} disabled={loading}>{loading ? "Submitting..." : "Submit Answer"}</button>
            </div>
          </div>
        </div>

        <aside style={{ borderRadius: 12, padding: 18, background: "var(--code-bg)", boxShadow: "var(--shadow)" }}>
          <h3>Session</h3>
          <p>Session ID: <code className="counter">{sessionId || "—"}</code></p>
          <p>Candidate: <strong>{candidateId}</strong></p>
          <div style={{ height: 12 }} />
          <div style={{ marginTop: 12 }}>
            <button onClick={() => {
              if (confirm("Are you sure you want to end the interview?")) nav("/results");
            }}>End Interview</button>
          </div>
        </aside>
      </div>
    </div>
  );
}
