from flask import Flask, jsonify, request, render_template
from threading import Timer
import time

app = Flask(__name__)



timers = {}
timer_status = {"is_running": False, "time_left": 0}



def start_timer(duration, timer_id):
    def timer_end():
        timer_status["is_running"] = False
        timer_status["time_left"] = 0
        print("Timer ended!")
        
    timer = Timer(duration, timer_end)
    timer.start()
    timers[timer_id] = timer
    timer_status["is_running"] = True
    timer_status["time_left"] = duration
    timer_status["start_time"] = time.time()






def stop_timer(timer_id):
    if timer_id in timers:
        timers[timer_id].cancel()
        timer_status["is_running"] = False
        timer_status["time_left"] = 0
        del timers[timer_id]






@app.route("/", methods=["GET"])
def index():
    return render_template("time.html")






@app.route("/start-timer", methods=["POST"])
def start_timer_endpoint():
    data = request.json
    duration = data.get("duration")
    timer_id = data.get("timer_id")

    if timer_status["is_running"]:
        return jsonify({"message": "A timer is already running"}), 400

    start_timer(duration, timer_id)
    return jsonify({"message": "Timer started", "timer_id": timer_id}), 200






@app.route("/stop-timer", methods=["POST"])
def stop_timer_endpoint():
    data = request.json
    timer_id = data.get("timer_id")

    if timer_id not in timers:
        return jsonify({"message": "No such timer running"}), 400

    stop_timer(timer_id)
    return jsonify({"message": "Timer stopped", "timer_id": timer_id}), 200






@app.route("/get-timer-status", methods=["GET"])
def get_timer_status_endpoint():
    if timer_status["is_running"]:
        elapsed_time = time.time() - timer_status["start_time"]
        time_left = max(0, timer_status["time_left"] - elapsed_time)
        return jsonify({"is_running": True, "time_left": time_left}), 200
    else:
        return jsonify({"is_running": False, "time_left": 0}), 200
    






if __name__ == "__main__":
    app.run(debug=True)