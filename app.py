from chatbot import app

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=4444,
            ssl_context=(app.config["SSL_CERT"], app.config["SSL_PRIV"]),
            debug=True)
