from flask import Flask, render_template, request, redirect, url_for, Response
from flask_ngrok import run_with_ngrok
import cv2

# Source 3

app = Flask(__name__)

camera = cv2.VideoCapture(0)

# Source 6
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["password"] != "pythonisfun":
            error = "Invalid Password. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("index.html", error=error)


# Source 7
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Static Feed':
            return redirect(url_for("static_vid"))
        elif request.form['submit_button'] == 'Live Feed':
            return redirect(url_for("live_feed"))
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('home.html')


@app.route("/static")
def static_vid():
    return render_template("static.html")


# Source 6
@app.route("/live")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/live_feed")
def live_feed():
    return render_template("live.html")


if __name__ == "__main__":
    app.run()

