import { useCallback, useEffect, useState } from "react";

function Exam() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(60);
  const [submitted, setSubmitted] = useState(false);
  const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

  // 🔐 Protect route
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) window.location.href = "/";
  }, []);

  // 📥 Fetch questions
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const token = localStorage.getItem("token");

        const res = await fetch(`${API}/questions`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();
        const shuffleArray = (array) => {
          return array
            .map((value) => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value);
        };

        setQuestions(shuffleArray(data));
      } catch {
        alert("Failed to load questions ❌");
      }
    };

    fetchQuestions();
  }, [API]);

  // 🧠 Select answer
  const handleSelect = (qid, option) => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [qid]: option }));
  };

  // 🚀 Submit
  const handleSubmit = useCallback(async () => {
    try {
      const token = localStorage.getItem("token");

      const formatted = {
        answers: Object.keys(answers).map((qid) => ({
          question_id: parseInt(qid),
          selected_option: answers[qid],
        })),
      };

      const res = await fetch(`${API}/submit-exam`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formatted),
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail);
        return;
      }

      const data = await res.json();

      window.location.href = `/result?score=${data.score}&total=${data.total}`;
      setSubmitted(true);
    } catch {
      alert("Submission failed ❌");
    }
  }, [answers, API]);

  // ⏱️ Timer
  useEffect(() => {
    if (submitted) return;

    if (timeLeft <= 0) {
      const timeout = setTimeout(() => {
        handleSubmit();
      }, 0);

      return () => clearTimeout(timeout);
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, submitted, handleSubmit]);

  return (
    <div className="flex min-h-screen bg-slate-900 text-white">
      {/* 📍 Sidebar */}
      <div className="w-64 bg-slate-800 p-4 border-r border-slate-700">
        <h2 className="text-lg font-bold mb-4">Questions</h2>

        <div className="grid grid-cols-4 gap-2">
          {questions.map((q, i) => (
            <div
              key={q.id}
              className={`p-2 text-center rounded cursor-pointer ${
                answers[q.id]
                  ? "bg-green-500"
                  : "bg-slate-700 hover:bg-slate-600"
              }`}
            >
              {i + 1}
            </div>
          ))}
        </div>
      </div>

      {/* 🔥 Main Content */}
      <div className="flex-1 p-8">
        {/* ⏱️ Timer */}
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">📝 Exam</h1>
          <div className="text-lg font-semibold bg-red-500 px-4 py-2 rounded">
            ⏱ {timeLeft}s
          </div>
        </div>

        {questions.map((q) => (
          <div key={q.id} className="bg-slate-800 p-6 mb-6 rounded-xl shadow">
            <p className="mb-4 font-semibold">{q.question_text}</p>

            {["option_a", "option_b", "option_c", "option_d"].map((opt) => (
              <label
                key={opt}
                className={`block p-2 rounded mb-2 cursor-pointer ${
                  answers[q.id] === q[opt]
                    ? "bg-blue-600"
                    : "bg-slate-700 hover:bg-slate-600"
                }`}
              >
                <input
                  type="radio"
                  name={`q-${q.id}`}
                  className="mr-2"
                  checked={answers[q.id] === opt}
                  onChange={() => handleSelect(q.id, opt)}
                />
                {q[opt]}
              </label>
            ))}
          </div>
        ))}

        {/* 🚀 Submit */}
        <button
          onClick={handleSubmit}
          disabled={submitted}
          className={`w-full py-3 rounded text-lg font-bold ${
            submitted ? "bg-gray-500" : "bg-green-500 hover:bg-green-600"
          }`}
        >
          {submitted ? "Submitted ✅" : "Submit Exam"}
        </button>
      </div>
    </div>
  );
}

export default Exam;
