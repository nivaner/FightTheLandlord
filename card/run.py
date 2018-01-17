from app import socketio, manage, app

# socketio.run(app, host='localhost')
socketio.run(app, host='0.0.0.0', port=3344)
# manage.run()
# app.run(debug=True, host='0.0.0.0')
