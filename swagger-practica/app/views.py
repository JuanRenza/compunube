# views.py

from flask import render_template
from app import app
from flask import abort
from flask import request

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
        return jsonify(spec.to_dict())

class booksResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        description = fields.Str()
        author = fields.Str()

class booksListResponseSchema(Schema):
        books_list = fields.List(fields.Nested(booksResponseSchema))

class deleteResponseSchema(Schema):
        result = fields.Bool()

books = [
    {
        'id': 1,
        'title': 'La hojarasca',
        'description': 'Good one', 
        'author': 'Gabo'
    },
    {
        'id': 2,
        'title': 'El coronel no tiene quien le escriba',
        'description': 'Interesting', 
        'author': 'Gabo'
    }
]

    

# Get all books
# For testing: curl -i http://localhost:5000/books 
@app.route('/books', methods=['GET'])
def get_books():
    """Get List of books
        ---
        get:
            description: Get List of books
            responses:
                200:
                    description: Return an books list
                    content:
                        application/json:
                            schema: booksListResponseSchema
    """
    return jsonify({'books': books})

# Get one book by id
# For testing: curl -i http://localhost:5000/books/2 
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a book
        ---
        get:
            description: Get a book
            responses:
                200:
                    description: Return a book
                    content:
                        application/json:
                            schema: booksResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

# Add new book
# For testing: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"El libro"}' http://localhost:5000/books
@app.route('/books', methods=['POST'])
def create_book():
    """Create a book
        ---
        post:
            description: Post a book
            responses:
                200:
                    description: Post a book
                    content:
                        application/json:
                            schema: booksResponseSchema
    """
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'author': request.json.get('author', ""),
    }
    books.append(book)
    return jsonify({'book': book}), 201

# Edit a Book
# For testing: curl -i -H "Content-Type: application/json" -X PUT -d '{"author":"Jorgito"}' http://localhost:5000/books/2
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Change a book
        ---
        put:
            description: Change a book
            responses:
                200:
                    description: Modify a book
                    content:
                        application/json:
                            schema: booksResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0 or not request.json:
        abort(404)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['description'] = request.json.get('description', book[0]['description'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    return jsonify({'book': book[0]})

# Delete a Book
# For testing: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/books/1
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book
        ---
        delete:
            description: Delete a book
            responses:
                200:
                    description: Book deleted
                    content:
                        application/json:
                            schema: deleteResponseSchema
                404:
                    description: Book not deleted
                    content:
                        application/json:
                            schema: deleteResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    resultado=True
    if len(book) == 0:
        abort(404)
        resultado = False
    books.remove(book[0])
    return jsonify({'result': resultado})

with app.test_request_context():
    spec.path(view=get_books)
    spec.path(view=get_book)
    spec.path(view=create_book)
    spec.path(view=update_book)
    spec.path(view=delete_book)


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html',base_url='/docs')
    else:
        return send_from_directory('static',path)










