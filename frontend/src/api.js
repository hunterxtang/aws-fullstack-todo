const base = (import.meta.env.VITE_API_BASE || "").replace(/\/$/, "")

export async function apiGet(path) {
  const r = await fetch(base + path)
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || "request failed")
  return data
}

export async function apiGetWeather() {
  return apiGet("/api/weather")
}

export async function apiPost(path, body) {
  const r = await fetch(base + path, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body)
  })
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || "request failed")
  return data
}

export async function apiPatch(path, body) {
  const r = await fetch(base + path, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body)
  })
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || "request failed")
  return data
}

export async function apiDelete(path) {
  const r = await fetch(base + path, { method: "DELETE" })
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || "request failed")
  return data
}
