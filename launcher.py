from flask import Flask, render_template
import subprocess
import threading
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/start-hand-detection')
def start_hand_detection():
    print("✅ Flask route triggered!")  # Check if this shows in terminal

    try:
        script_path = os.path.join(os.getcwd(), "test.py")
        print("👉 Running:", script_path)
        subprocess.Popen(["python", script_path])
        return "Hand Detection Started!"
    except Exception as e:
        print("❌ Error launching main.py:", e)
        return f"Failed: {e}"



def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
