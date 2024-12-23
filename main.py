from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from uuid import uuid4

app = FastAPI()

# 사용자 세션 관리
sessions = {}

# HTML과 JS를 포함한 엔드포인트
@app.get("/", response_class=HTMLResponse)
async def read_html(request: Request):
    # 세션 체크
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        user_name = sessions[session_id]["user_name"]
    else:
        user_name = None

    # HTML 콘텐츠 반환
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI with Login, Logout, Todo</title>
    </head>
    <body>
        <h1>Welcome to FastAPI Web Application</h1>

        <!-- 로그인/로그아웃 상태 표시 -->
        <div id="loginStatus">
            {"<p>Logged in as " + user_name + "</p>" if user_name else "<p>You are not logged in.</p>"}
        </div>

        <!-- 로그인 폼 -->
        <div id="loginForm" style="display: {'none' if user_name else 'block'};">
            <h3>Login</h3>
            <input type="text" id="username" placeholder="Enter your name" />
            <button onclick="login()">Login</button>
        </div>

        <!-- 로그아웃 버튼 -->
        <div id="logoutButton" style="display: {'block' if user_name else 'none'};">
            <button onclick="logout()">Logout</button>
        </div>

        <!-- 투두리스트 -->
        <h3>Your Todo List</h3>
        <input type="text" id="todoInput" placeholder="Add a new task">
        <button onclick="addTodo()">Add Todo</button>
        <ul id="todoList"></ul>

        <script>
            let userName = "{user_name}";

            // 로그인 기능
            function login() {{
                userName = document.getElementById("username").value;
                if (userName) {{
                    document.cookie = "session_id=" + userName + "; path=/";
                    location.reload();
                }}
            }}

            // 로그아웃 기능
            function logout() {{
                document.cookie = "session_id=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
                location.reload();
            }}

            // 투두리스트 관리
            const todoList = JSON.parse(localStorage.getItem('todos')) || [];

            function renderTodos() {{
                const todoListElement = document.getElementById("todoList");
                todoListElement.innerHTML = "";
                todoList.forEach((todo, index) => {{
                    const li = document.createElement("li");
                    li.textContent = todo;
                    const deleteBtn = document.createElement("button");
                    deleteBtn.textContent = "Delete";
                    deleteBtn.onclick = function() {{
                        deleteTodo(index);
                    }};
                    li.appendChild(deleteBtn);
                    todoListElement.appendChild(li);
                }});
            }}

            function addTodo() {{
                const todoInput = document.getElementById("todoInput");
                const todoText = todoInput.value;
                if (todoText) {{
                    todoList.push(todoText);
                    localStorage.setItem('todos', JSON.stringify(todoList));
                    todoInput.value = "";
                    renderTodos();
                }}
            }}

            function deleteTodo(index) {{
                todoList.splice(index, 1);
                localStorage.setItem('todos', JSON.stringify(todoList));
                renderTodos();
            }}

            renderTodos();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 로그인 처리 엔드포인트
@app.post("/login/")
async def login(request: Request, username: str):
    session_id = str(uuid4())
    sessions[session_id] = {"user_name": username}
    response = HTMLResponse(content="Logged in")
    response.set_cookie(key="session_id", value=session_id)
    return response

# 로그아웃 처리 엔드포인트
@app.post("/logout/")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]
    response = HTMLResponse(content="Logged out")
    response.delete_cookie(key="session_id")
    return response