import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Simple in-memory storage (demo ke liye database ki zaroorat nahi)
tasks = []
next_id = 1


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/info")
def info():
    return jsonify(
        message="Task Manager API chal rahi hai",
        env=os.environ.get("APP_ENV", "development"),
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def add_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title required hai"), 400
    task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify(error="task nahi mila"), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify(message="deleted")
    return jsonify(error="task nahi mila"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)