from operators_backend.app import create_app

application = create_app()
application.run(debug=True)