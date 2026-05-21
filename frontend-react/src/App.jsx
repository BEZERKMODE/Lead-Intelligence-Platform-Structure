import { useState } from 'react'

const BACKEND_URL = 'http://localhost:5003'

function App() {
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch(`${BACKEND_URL}/enterprise-intelligence/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          company_name: 'Example Ltd',
          domain: 'example.com',
          city: 'Bangalore',
          state: 'Karnataka'
        })
      })

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`)
      }

      const data = await res.json()
      setResponse(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="card">
        <h1>Lead Intelligence Platform</h1>
        <p>Frontend is now scaffolded and ready to run.</p>
        <button onClick={runAnalysis} disabled={loading}>
          {loading ? 'Analyzing...' : 'Run sample enterprise analysis'}
        </button>
        {error && <div className="message error">{error}</div>}
        {response && (
          <div className="message success">
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
        <div className="note">
          Use <strong>http://localhost:5173</strong> to access the frontend, and the backend is expected at <strong>http://localhost:5003</strong>.
        </div>
      </div>
    </div>
  )
}

export default App
