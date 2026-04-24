import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Leaderboard() {
  const [data, setData] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/leaderboard")
        const result = await res.json()
        setData(result)
      } catch (err) {
        alert("Failed to load leaderboard ❌")
      }
    }

    fetchLeaderboard()
  }, [])

  return (
    <div className="container">

      {/* Sidebar */}
      <div className="sidebar">
        <h2>🧠 ExamApp</h2>
        <button onClick={() => navigate("/dashboard")}>Dashboard</button>
      </div>

      {/* Main */}
      <div className="main">

        <div className="navbar">
          <h3>🏆 Leaderboard</h3>
        </div>

        <div className="card">
          {data.length === 0 ? (
            <p>Loading...</p>
          ) : (
            data.map((user, index) => (
              <div key={index} style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "10px",
                borderBottom: "1px solid #1e293b"
              }}>
                <span>#{index + 1} {user.user_email}</span>
                <span>{user.score}</span>
              </div>
            ))
          )}
        </div>

      </div>
    </div>
  )
}

export default Leaderboard