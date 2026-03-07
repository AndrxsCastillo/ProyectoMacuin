from app import create_app

app = create_app()

if __name__ == '__main__':
    # Flask correrá en el puerto 5000 para no chocar con FastAPI (8000)
    app.run(debug=True, host='0.0.0.0', port=5000)