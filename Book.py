from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(_name_)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

books=[]

@app.route("/")
@cross_origin()
def greet():
    return "<p>Welcome to Book Management System</p>"

@app.route("/books", methods=["GET"])
@cross_origin()
def get_all_books():
    return jsonify({"books": books})

@app.route("/books/<int:book_id>", methods=["GET"])
@cross_origin()
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route("/books", methods=["POST"])
@cross_origin()
def create_book():
    data = request.get_json()
    if 'title' not in data or 'author' not in data:
        return jsonify({"error": "Missing title or author"}), 400

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/books/<int:book_id>", methods=["PUT"])
@cross_origin()
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    return jsonify(book)

@app.route("/books/<int:book_id>", methods=["DELETE"])
@cross_origin()
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)