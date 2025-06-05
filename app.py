from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows API calls if you want to access from another origin

tasks = []
task_id = 1

# The HTML frontend served by Flask
HTML_PAGE = HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>🌈 Colorful To-Do App</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #667eea, #764ba2);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 50px 20px;
      color: #fff;
    }
    .container {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(12px);
      border-radius: 20px;
      width: 100%;
      max-width: 480px;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
      padding: 30px 40px;
    }
    h1 {
      font-weight: 600;
      text-align: center;
      margin-bottom: 30px;
      letter-spacing: 2px;
      text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .input-group {
      display: flex;
      margin-bottom: 25px;
    }
    input[type="text"] {
      flex-grow: 1;
      padding: 14px 20px;
      border-radius: 50px 0 0 50px;
      border: none;
      font-size: 16px;
      outline: none;
      color: #333;
      transition: box-shadow 0.3s ease;
    }
    input[type="text"]:focus {
      box-shadow: 0 0 10px #ff6a00;
    }
    button {
      background: #ff6a00;
      border: none;
      padding: 0 25px;
      border-radius: 0 50px 50px 0;
      color: white;
      font-weight: 600;
      cursor: pointer;
      font-size: 16px;
      transition: background 0.3s ease, transform 0.2s ease;
      box-shadow: 0 4px 12px rgba(255, 106, 0, 0.6);
    }
    button:hover {
      background: #ff8c33;
      transform: scale(1.05);
      box-shadow: 0 6px 20px rgba(255, 140, 51, 0.7);
    }
    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      max-height: 350px;
      overflow-y: auto;
    }
    li {
      background: rgba(255, 255, 255, 0.25);
      margin-bottom: 15px;
      padding: 12px 20px;
      border-radius: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #333;
      font-weight: 600;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      transition: background 0.3s ease;
      cursor: default;
    }
    li:hover {
      background: #ff6a0044;
      color: white;
      box-shadow: 0 6px 15px rgba(255, 106, 0, 0.5);
    }
    .delete-btn {
      background: #e53e3e;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      border: none;
      color: white;
      font-weight: 700;
      cursor: pointer;
      font-size: 18px;
      line-height: 0;
      transition: background 0.3s ease, transform 0.2s ease;
      box-shadow: 0 3px 10px rgba(229, 62, 62, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .delete-btn:hover {
      background: #c53030;
      transform: scale(1.1);
      box-shadow: 0 5px 15px rgba(197, 48, 48, 0.7);
    }
    /* Scrollbar styling for task list */
    ul::-webkit-scrollbar {
      width: 8px;
    }
    ul::-webkit-scrollbar-track {
      background: transparent;
    }
    ul::-webkit-scrollbar-thumb {
      background: #ff6a00;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1> My To-Do List</h1>
    <div class="input-group">
      <input type="text" id="taskInput" placeholder="What’s your next task?" autocomplete="off" />
      <button onclick="addTask()">Add</button>
    </div>
    <ul id="taskList" aria-live="polite" aria-label="To-Do List"></ul>
  </div>

  <script>
    const apiUrl = "";

    function fetchTasks() {
      fetch(`${apiUrl}/tasks`)
        .then(response => response.json())
        .then(data => {
          const list = document.getElementById("taskList");
          list.innerHTML = "";
          if(data.length === 0){
            list.innerHTML = '<li style="text-align:center; color: #eee; font-style: italic;">No tasks yet! Add one above ✨</li>';
            return;
          }
          data.forEach(task => {
            const li = document.createElement("li");
            li.innerHTML = `
              ${task.task}
              <button class="delete-btn" aria-label="Delete task: ${task.task}" onclick="confirmDelete(${task.id})">&times;</button>
            `;
            list.appendChild(li);
          });
        })
        .catch(() => {
          const list = document.getElementById("taskList");
          list.innerHTML = '<li style="text-align:center; color: #ff6a0044;">Error loading tasks :(</li>';
        });
    }

    function addTask() {
      const input = document.getElementById("taskInput");
      const task = input.value.trim();
      if(!task) {
        alert("Please enter a task");
        input.focus();
        return;
      }
      fetch(`${apiUrl}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task })
      })
      .then(response => {
        if (!response.ok) throw new Error("Failed to add task");
        return response.json();
      })
      .then(() => {
        input.value = "";
        input.focus();
        fetchTasks();
      })
      .catch(e => alert(e.message));
    }

    function confirmDelete(id) {
      if(confirm("Are you sure you want to delete this task?")) {
        deleteTask(id);
      }
    }

    function deleteTask(id) {
      fetch(`${apiUrl}/delete/${id}`, { method: "DELETE" })
        .then(() => fetchTasks());
    }

    document.getElementById("taskInput").addEventListener("keydown", function(event) {
      if(event.key === "Enter") {
        addTask();
      }
    });

    // Load tasks on page load
    fetchTasks();
  </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    global task_id
    data = request.get_json()
    task_text = data.get('task', '').strip()
    if not task_text:
        return jsonify({'error': 'Task cannot be empty'}), 400
    task = {'id': task_id, 'task': task_text}
    tasks.append(task)
    task_id += 1
    return jsonify(task), 201

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)

