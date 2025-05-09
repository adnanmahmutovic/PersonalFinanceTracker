from flask import Flask, jsonify, request
from db_config import get_db_connection

app = Flask(__name__)

# Income Route One
@app.route('/income', methods=['GET'])
def get_income():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, amount, date FROM income")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    income_data = []
    for row in rows:
        income_data.append({
            'id': row[0],
            'source': row[1],
            'amount': float(row[2]),
            'date': row[3].strftime('%Y-%m-%d')
        })

    return jsonify(income_data)

# Income Route Two
@app.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO income (source, amount, date) VALUES (%s, %s, %s)"
    values = (data['source'], data['amount'], data['date'])
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Income added successfully!'}), 201

# Expenses Route One
@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, date FROM expenses")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    expenses_data = []
    for row in rows:
        expenses_data.append({
            'id': row[0],
            'category': row[1],
            'amount': float(row[2]),
            'date': row[3].strftime('%Y-%m-%d')
        })
    return jsonify(expenses_data)


# Expenses Route Two
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)",
        (data['category'], data['amount'], data['date'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Expense added successfully!'}), 201


# Summary Route
@app.route('/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    # calculating total income
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM income")
    total_income = float(cursor.fetchone()[0])

    # calculating total expenses
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_expenses = float(cursor.fetchone()[0])

    # closing the connection
    cursor.close()
    conn.close()

    # computing the remaining balance
    balance = total_income - total_expenses

    return jsonify({
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance
    })

if __name__ == '__main__':
    app.run(debug=True)
