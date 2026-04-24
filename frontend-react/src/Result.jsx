import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import Confetti from "react-confetti"

function Result() {
  const navigate = useNavigate()
  const [params] = useSearchParams()

  const scoreParam = params.get("score")
  const totalParam = params.get("total")

  const [displayScore, setDisplayScore] = useState(0)

  // 🔐 Protect route
  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) navigate("/")
  }, [navigate])

  // ❌ If accessed directly without data
  if (!scoreParam || !totalParam) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        <p className="text-lg">No result data found ❌</p>
      </div>
    )
  }

  const score = parseInt(scoreParam)
  const total = parseInt(totalParam)

  const percentage = Math.round((score / total) * 100)
  const passed = percentage >= 40

  // 🎬 Score animation
  useEffect(() => {
    let current = 0

    const interval = setInterval(() => {
      if (current >= score) {
        clearInterval(interval)
      } else {
        current++
        setDisplayScore(current)
      }
    }, 40)

    return () => clearInterval(interval)
  }, [score])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 text-white">

      {/* 🎉 Confetti */}
      {passed && displayScore === score && (
        <Confetti numberOfPieces={200} />
      )}

      <div className="bg-slate-900 p-10 rounded-2xl shadow-xl border border-slate-700 text-center w-96 transform hover:scale-105 transition duration-300">

        {/* 🎯 Score */}
        <h1 className={`text-5xl font-bold mb-4 ${
          passed ? "text-green-400" : "text-red-400"
        }`}>
          {displayScore}/{total}
        </h1>

        {/* 📊 Percentage */}
        <p className="text-xl mb-4">
          {percentage}% Score
        </p>

        {/* 📊 Progress Bar */}
        <div className="w-full bg-slate-700 rounded-full h-3 mb-6">
          <div
            className="bg-blue-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${percentage}%` }}
          ></div>
        </div>

        {/* 🟢 Pass / Fail */}
        <div
          className={`mb-6 text-lg font-semibold px-4 py-2 rounded ${
            passed ? "bg-green-500" : "bg-red-500"
          }`}
        >
          {passed ? "✅ Passed" : "❌ Failed"}
        </div>

        {/* 💬 Message */}
        <p className="text-slate-400 mb-8">
          {passed
            ? "Great job! Keep improving 🚀"
            : "Don’t worry, try again 💪"}
        </p>

        {/* 🔘 Buttons */}
        <div className="flex gap-4">

          <button
            onClick={() => navigate("/dashboard")}
            className="flex-1 bg-slate-700 hover:bg-slate-600 p-3 rounded-lg"
          >
            Dashboard
          </button>

          <button
            onClick={() => navigate("/exam")}
            className="flex-1 bg-blue-600 hover:bg-blue-700 p-3 rounded-lg"
          >
            Retake
          </button>

        </div>

      </div>
    </div>
  )
}

export default Result

