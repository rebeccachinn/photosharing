from flaskblog import app
# from flaskblog import app, socketio

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)