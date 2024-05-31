from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/transactions')
def hello():
    # return 'Hello World!'
    return render_template('index.html')


@app.route('/approvals', methods=['POST', 'GET'])
def submit():
    return render_template('approvals.html')



if __name__ == '__main__':
    app.run(debug=True)