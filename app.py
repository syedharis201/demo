from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Task storage with status
tasks = []

@app.route('/')
def index():
    # Filter tasks based on the status
    filter_status = request.args.get('filter', 'all')
    if filter_status == 'completed':
        filtered_tasks = [task for task in tasks if task['completed']]
    elif filter_status == 'pending':
        filtered_tasks = [task for task in tasks if not task['completed']]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, filter_status=filter_status)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    if task_name:
        tasks.append({'name': task_name, 'completed': False})
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 0 <= task_id < len(tasks):
        new_name = request.form.get('new_name')
        if new_name:
            tasks[task_id]['name'] = new_name
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
