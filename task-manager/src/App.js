import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState(() => {
    const savedTasks = localStorage.getItem('tasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });
  const [input, setInput] = useState('');
  const [filter, setFilter] = useState('all');

  // Save tasks to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  const addTask = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;
    
    const newTask = {
      id: Date.now(),
      text: input,
      completed: false
    };
    
    setTasks([...tasks, newTask]);
    setInput('');
  };

  const toggleTask = (id) => {
    setTasks(tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const tasksLeft = tasks.filter(task => !task.completed).length;

  return (
    <div className="app">
      <div className="container">
        <h1>Task Manager</h1>
        
        <form onSubmit={addTask} className="task-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Add a new task..."
            className="task-input"
          />
          <button type="submit" className="add-button">Add Task</button>
        </form>

        <div className="filters">
          <button 
            onClick={() => setFilter('all')}
            className={filter === 'all' ? 'active' : ''}
          >
            All
          </button>
          <button 
            onClick={() => setFilter('active')}
            className={filter === 'active' ? 'active' : ''}
          >
            Active
          </button>
          <button 
            onClick={() => setFilter('completed')}
            className={filter === 'completed' ? 'active' : ''}
          >
            Completed
          </button>
        </div>

        <div className="task-list">
          {filteredTasks.map(task => (
            <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task.id)}
                className="task-checkbox"
              />
              <span className="task-text">{task.text}</span>
              <button 
                onClick={() => deleteTask(task.id)}
                className="delete-button"
              >
                ×
              </button>
            </div>
          ))}
        </div>

        <div className="task-stats">
          {tasksLeft} {tasksLeft === 1 ? 'task' : 'tasks'} left
        </div>
      </div>
    </div>
  );
}

export default App;
