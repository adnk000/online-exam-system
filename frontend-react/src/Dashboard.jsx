import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard() {
  const navigate = useNavigate()

  // 🔐 Protect route
  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      navigate("/")
    }
  }, [navigate])

  const startExam = () => {
    navigate("/exam")
  }

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">

      {/* 🔝 Navbar */}
      <div className="flex justify-between items-center px-8 py-4 bg-slate-900 border-b border-slate-700 shadow-lg">
        <h1 className="text-xl font-bold">🧠 Online Exam System</h1>
        <button
          onClick={logout}
          className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition"
        >
          Logout
        </button>
      </div>

      {/* 🔥 Main Content */}
      <div className="p-8">

        {/* 👋 Welcome */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Welcome back 👋</h2>
          <p className="text-slate-400">Ready to take your exam?</p>
        </div>

        {/* 📊 Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

          <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-md hover:scale-105 transition">
            <h3 className="text-slate-400">Total Exams</h3>
            <p className="text-2xl font-bold mt-2">5</p>
          </div>

          <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-md hover:scale-105 transition">
            <h3 className="text-slate-400">Completed</h3>
            <p className="text-2xl font-bold mt-2">2</p>
          </div>

          <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-md hover:scale-105 transition">
            <h3 className="text-slate-400">Best Score</h3>
            <p className="text-2xl font-bold mt-2">80%</p>
          </div>

        </div>

        {/* 🚀 Start Exam Card */}
        <div className="flex justify-center">
          <div className="bg-slate-900 p-10 rounded-2xl border border-slate-700 shadow-xl text-center w-full max-w-md">

            <h3 className="text-xl font-semibold mb-4">Take a New Exam</h3>
            <p className="text-slate-400 mb-6">
              Test your knowledge and improve your skills.
            </p>

            <button
              onClick={startExam}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg text-lg font-semibold transition"
            >
              🚀 Start Exam
            </button>

          </div>
        </div>

      </div>
    </div>
  )
}

export default Dashboard