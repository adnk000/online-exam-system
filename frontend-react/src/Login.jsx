import { useState } from "react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const API = import.meta.env.VITE_API_URL

  const handleLogin = async () => {
    try {
      const res = await fetch('${API}/login', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (!res.ok) throw new Error();

      const data = await res.json();
      localStorage.setItem("token", data.access_token);

      window.location.href = "/dashboard";
    } catch {
      alert("Login failed ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="bg-slate-900/70 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-80 border border-slate-700">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          🔐 Login
        </h2>

        <input
          type="email"
          placeholder="Email"
          value={email || ""}
          className="w-full mb-4 p-3 rounded-lg bg-slate-800 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password || ""}
          className="w-full mb-4 p-3 rounded-lg bg-slate-800 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 transition p-3 rounded-lg font-semibold"
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;
