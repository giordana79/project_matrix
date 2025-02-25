from app import app
from flask import request, jsonify
from app.tasks import run_agent1_task, run_agent2_task, run_agent3_task, run_agent4_task

@app.route('/run_agent1', methods=['POST'])
def run_agent1():
    data = request.json.get('data')
    task = run_agent1_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent2', methods=['POST'])
def run_agent2():
    data = request.json.get('data')
    task = run_agent2_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent3', methods=['POST'])
def run_agent3():
    data = request.json.get('data')
    task = run_agent3_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent4', methods=['POST'])
def run_agent4():
    data = request.json.get('data')
    task = run_agent4_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)