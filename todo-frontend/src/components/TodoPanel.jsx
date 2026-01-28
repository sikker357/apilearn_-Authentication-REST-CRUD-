import React, { useState, useEffect } from "react";
import { fetchTodos, addTodo } from "../api";

export default function TodoPanel() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState("");

  useEffect(() => {
    const loadTodos = async () => {
      try {
        const data = await fetchTodos();
        setTodos(data);
      } catch (err) {
        console.error("Error fetching todos:", err);
      }
    };
    loadTodos();
  }, []);

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const created = await addTodo({ title: newTodo });
      setTodos([...todos, created]);
      setNewTodo("");
    } catch (err) {
      console.error("Error adding todo:", err);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white shadow rounded-xl">
      <h2 className="text-xl font-bold mb-4">Todo Panel</h2>
      <form onSubmit={handleAddTodo} className="flex gap-2 mb-4">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Add new todo"
          className="flex-1 p-2 border rounded-lg"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Add
        </button>
      </form>
      <ul className="space-y-2">
        {todos.map((todo) => (
          <li
            key={todo.id}
            className="p-2 border rounded-lg flex justify-between"
          >
            <span>{todo.title}</span>
            <span>{todo.completed ? "✅" : "❌"}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
