from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# course 100 days of code

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book-collection.db"

db = SQLAlchemy(app)

# CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False )
    rating = db.Column(db.Float, nullable=False )

    def __repr__(self) -> str:
        return f'<Book {self.title!r}>'


@app.route('/')
def home():
    with app.app_context():
        db.create_all()

        # READ ALL RECORDS
        all_books = db.session.query(Book).all()

    return render_template('index.html', books=all_books)


@app.route("/add",  methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # CRETE RECORD
        new_book = Book(
                title = request.form.get('title'),
                author = request.form.get('author'),
                rating = request.form.get('rating'),
                )
        
        db.session.add(new_book)
        db.session.commit()

        return redirect( url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    book_id = request.args.get('id', type=int)
    book_selected = db.session.query(Book).get(book_id)
    
    if request.method == 'POST':
        # UPDATE RECORD

        new_rating = request.form.get('value_update', type=float)
        
        print('book id >>', new_rating)

        db.session.query(Book).filter_by(id=book_id).\
            update({'rating': new_rating})
        db.session.commit()
            
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=book_selected)


@app.route('/delet', methods=['GET'])
def delet():
    book_id = request.args.get(key='id', type=int)

    # DELETE RECORD
    db.session.query(Book).filter_by(id=book_id).\
        delete()
    db.session.commit()

    return redirect(url_for('home'))        


if __name__ == "__main__":
    app.run(debug=True)
    