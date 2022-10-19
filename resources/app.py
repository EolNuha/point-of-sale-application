from website import create_app

app = create_app()

if __name__ == '__main__':
    #Make sure to remove debug=True when create exe
    app.run(debug=True)