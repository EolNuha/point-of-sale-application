from website import create_app

app = create_app()

if __name__ == '__main__':
    #Make sure to remove debug=True when creating .exe file
    app.run(debug=True, host="127.0.0.1", port=5000)