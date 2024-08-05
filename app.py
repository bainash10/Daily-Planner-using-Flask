from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Example data structure to store tasks with time slots
tasks = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_task' in request.form:
            time_slot = request.form.get('time_slot')
            task_description = request.form.get('task_description')
            if time_slot and task_description:
                task = {'time_slot': time_slot, 'description': task_description}
                tasks.append(task)
                flash('Task added successfully!', 'success')
            else:
                flash('Please fill in all fields.', 'danger')
        elif 'edit_task' in request.form:
            task_id_str = request.form.get('task_id')
            time_slot = request.form.get('time_slot')
            task_description = request.form.get('task_description')
            if task_id_str:
                try:
                    task_id = int(task_id_str)
                    if 0 <= task_id < len(tasks):
                        if time_slot and task_description:
                            tasks[task_id] = {'time_slot': time_slot, 'description': task_description}
                            flash('Task updated successfully!', 'success')
                        else:
                            flash('Please fill in all fields.', 'danger')
                    else:
                        flash('Invalid task ID.', 'danger')
                except ValueError:
                    flash('Invalid task ID format.', 'danger')
            else:
                flash('Task ID cannot be empty.', 'danger')
        return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        flash('Task deleted successfully!', 'success')
    else:
        flash('Invalid task ID.', 'danger')
    return redirect(url_for('index'))

@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html', tasks=tasks)

@app.route('/routine')
def routine_view():
    return render_template('routine.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
