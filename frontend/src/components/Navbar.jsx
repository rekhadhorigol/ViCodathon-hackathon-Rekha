import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

function getInitialTheme() {
  const saved = localStorage.getItem("intmate.theme");
  if (saved === "dark" || saved === "light") return saved;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export default function Navbar() {
  const loc = useLocation();
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("theme-light", "theme-dark");
    root.classList.add(theme === "dark" ? "theme-dark" : "theme-light");
    localStorage.setItem("intmate.theme", theme);
  }, [theme]);

  return (
    <header style={styles.header}>
      <div style={styles.brand}>
        <div style={styles.logo}>I</div>
        <div>
          <div style={styles.title}>Intmate</div>
          <div style={styles.subtitle}>Your AI Interview Agent</div>
        </div>
      </div>

      <nav style={styles.nav}>
        <Link to="/" style={linkStyle(loc.pathname === "/")}>Home</Link>
        <Link to="/setup" style={linkStyle(loc.pathname === "/setup")}>Start</Link>
        <Link to="/results" style={linkStyle(loc.pathname === "/results")}>Results</Link>
        <button
          type="button"
          className="theme-toggle"
          onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
        >
          {theme === "dark" ? "☀️" : "🌙"}
        </button>
      </nav>
    </header>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "18px 28px",
    borderBottom: "1px solid var(--border)",
    background: "linear-gradient(90deg, rgba(170,59,255,0.03), transparent)",
    flexWrap: "wrap",
    gap: 12,
  },
  brand: { display: "flex", gap: 12, alignItems: "center" },
  logo: {
    width: 44,
    height: 44,
    borderRadius: 10,
    background: "linear-gradient(135deg,#6b46c1,#4f46e5)",
    color: "white",
    display: "grid",
    placeItems: "center",
    fontWeight: 700,
    fontSize: 20,
  },
  title: { fontWeight: 700, color: "var(--text-h)" },
  subtitle: { fontSize: 12, color: "var(--text)" },
  nav: { display: "flex", gap: 12, alignItems: "center" },
};

function linkStyle(active) {
  return {
    padding: "8px 14px",
    borderRadius: 8,
    textDecoration: "none",
    color: active ? "white" : "var(--text-h)",
    background: active ? "linear-gradient(90deg,#4f46e5,#6b46c1)" : "transparent",
    boxShadow: active ? "var(--shadow)" : "none",
  };
}
