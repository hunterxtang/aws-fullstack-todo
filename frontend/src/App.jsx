import React, { useEffect, useMemo, useState } from "react"
import { apiDelete, apiGet, apiPatch, apiPost } from "./api.js"

export default function App() {
  const [items, setItems] = useState([])
  const [text, setText] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const remaining = useMemo(() => items.filter(x => !x.done).length, [items])

  async function refresh() {
    setLoading(true)
    setError("")
    try {
      const data = await apiGet("/api/todos")
      setItems(data.items || [])
    } catch (e) {
      setError(String(e.message || e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  async function onAdd(e) {
    e.preventDefault()
    setError("")
    const t = text.trim()
    if (t.length === 0) return
    try {
      await apiPost("/api/todos", { text: t })
      setText("")
      await refresh()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  async function onToggle(item) {
    setError("")
    try {
      await apiPatch("/api/todos/" + item.id, { done: !item.done })
      await refresh()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  async function onDelete(item) {
    setError("")
    try {
      await apiDelete("/api/todos/" + item.id)
      await refresh()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  return (
    <div className="page">
      <div className="card">
        <div className="header">
          <h1>Todo</h1>
          <div className="meta">{remaining} remaining</div>
        </div>

        <form onSubmit={onAdd} className="row">
          <input
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Add a task…"
          />
          <button type="submit">Add</button>
        </form>

        {error ? <div className="error">{error}</div> : null}
        {loading ? <div className="muted">Loading…</div> : null}

        <div className="list">
          {items.map(item => (
            <div key={item.id} className="item">
              <label className="check">
                <input
                  type="checkbox"
                  checked={item.done}
                  onChange={() => onToggle(item)}
                />
                <span className={item.done ? "done" : ""}>{item.text}</span>
              </label>
              <button className="danger" onClick={() => onDelete(item)}>
                Delete
              </button>
            </div>
          ))}
        </div>

        <div className="footer">
          <button className="ghost" onClick={refresh}>Refresh</button>
        </div>
      </div>
    </div>
  )
}
