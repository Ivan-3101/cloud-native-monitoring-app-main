import psutil
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    cpu_metric = psutil.cpu_percent()
    mem_metric = psutil.virtual_memory().percent
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'username': proc.info['username']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    Message = None
    if cpu_metric > 80 or mem_metric > 80:
        Message = "High CPU or Memory Detected, scale up!!!"
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=Message, processes=processes)

@app.route("/kill_process", methods=["POST"])
def kill_process():
    pid = request.form.get("pid")
    if pid:
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
            return redirect(url_for("index"))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')