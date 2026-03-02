from flask import Flask, render_template, request, redirect
import sqlite3
import os

if not os.path.exists('database.db'):
    import init_db

app = Flask(__name__, template_folder='../templates', static_folder='../static')

def connect_db():
    return sqlite3.connect('database.db')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    farmer = request.form['farmer']
    crop = request.form['crop']
    quantity = request.form['quantity']
    price = request.form['price']

    conn = connect_db()
    c = conn.cursor()

    c.execute("INSERT INTO farmers (name, location) VALUES (?, ?)", (farmer, "Local"))
    farmer_id = c.lastrowid

    c.execute("INSERT INTO crops (farmer_id, crop_name, quantity, expected_price) VALUES (?, ?, ?, ?)",
              (farmer_id, crop, quantity, price))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/buyer')
def buyer():
    conn = connect_db()
    c = conn.cursor()

    crops = c.execute("SELECT * FROM crops").fetchall()
    conn.close()

    return render_template('buyer.html', crops=crops)

@app.route('/offer', methods=['POST'])
def offer():
    buyer = request.form['buyer']
    crop_id = request.form['crop_id']
    price = request.form['price']

    conn = connect_db()
    c = conn.cursor()

    c.execute("INSERT INTO buyers (name, location) VALUES (?, ?)", (buyer, "Local"))
    buyer_id = c.lastrowid

    c.execute("INSERT INTO offers (buyer_id, crop_id, offered_price) VALUES (?, ?, ?)",
              (buyer_id, crop_id, price))

    conn.commit()
    conn.close()

    return redirect('/buyer')

@app.route('/offers')
def view_offers():
    conn = connect_db()
    c = conn.cursor()

    offers = c.execute("""
        SELECT offers.id, crops.crop_name, offers.offered_price, offers.status
        FROM offers
        JOIN crops ON offers.crop_id = crops.id
    """).fetchall()

    conn.close()
    return render_template('offers.html', offers=offers)

@app.route('/accept/<id>')
def accept(id):
    conn = connect_db()
    c = conn.cursor()

    c.execute("UPDATE offers SET status='Accepted' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/offers')
    
    def handler(request):
        return app(request)
