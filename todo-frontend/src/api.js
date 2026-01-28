const API_URL = "http://127.0.0.1:8000";  // FastAPI backend

// Get all todos
export async function fetchTodos() {
  const res = await fetch(`${API_URL}/todos`);
  return res.json();
}

// Add a todo
export async function addTodo(todo, token) {
  const res = await fetch(`${API_URL}/todos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token && { "Authorization": `Bearer ${token}` }) // for protected endpoints
    },
    body: JSON.stringify(todo)
  });
  return res.json();
}
