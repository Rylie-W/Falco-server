from src.detector import app

@app.route("/hello")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        use_reloader=False)