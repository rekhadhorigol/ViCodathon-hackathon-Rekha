import mockApi from "./mockApi";

// In development use the Vite proxy (relative paths) to avoid CORS issues.
const API_BASE = import.meta.env.DEV ? "" : import.meta.env.VITE_API_BASE || "";
const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === "true";

async function postJson(url, body) {
  const res = await fetch(API_BASE + url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }

  return res.json();
}

async function getJson(url) {
  const res = await fetch(API_BASE + url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

function startInterview(payload) {
  if (USE_MOCK_API) {
    return Promise.resolve(mockApi.startInterview(payload));
  }
  return postJson("/api/interview", payload);
}

function evaluate(payload) {
  if (USE_MOCK_API) {
    return Promise.resolve(mockApi.evaluate(payload));
  }
  return postJson("/evaluate", payload);
}

function evaluateOverall(payload) {
  if (USE_MOCK_API) {
    return Promise.resolve(mockApi.evaluateOverall(payload));
  }
  return postJson("/evaluate/overall", payload);
}

function getResult(sessionId) {
  if (USE_MOCK_API) {
    return Promise.resolve(mockApi.getResult(sessionId));
  }
  return getJson(`/api/interview/${sessionId}/result`);
}

export default {
  startInterview,
  evaluate,
  evaluateOverall,
  getResult,
};
