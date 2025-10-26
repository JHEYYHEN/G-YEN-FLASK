from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ---------------------------
# Mock Student Database
# ---------------------------
students = [
    {"id": 1, "name": "Gyen May", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Mikay", "grade": 10, "section": "Daniel"},
    {"id": 3, "name": "Yenyen", "grade": 9, "section": "Ezekiel"},
]

# ---------------------------
# Home Page (Styled)
# ---------------------------
@app.route('/')
def home():
    html = """
    <html>
    <head>
        <title>Student API Portal</title>
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #007bff, #6610f2);
                color: white;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 {
                font-size: 45px;
                margin-top: 80px;
                letter-spacing: 1px;
            }
            p {
                font-size: 18px;
                color: #f0f0f0;
                margin-bottom: 40px;
            }
            .btn {
                display: inline-block;
                margin: 10px;
                padding: 15px 25px;
                border-radius: 10px;
                background-color: white;
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn:hover {
                background: #f8f9fa;
                transform: scale(1.05);
            }
            .footer {
                margin-top: 100px;
                font-size: 14px;
                color: #ccc;
            }
        </style>
    </head>
    <body>
        <h1>🎓 Welcome to the Student Management API</h1>
        <p>Manage student data with an interactive interface and API endpoints.</p>
        <a class="btn" href="/students">📋 View All Students</a>
        <a class="btn" href="/add">➕ Add New Student</a>
        <div class="footer">
            Developed with ❤️ using Flask
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------------------------
# All Students Page (Styled Table)
# ---------------------------
@app.route('/students', methods=['GET'])
def get_students():
    table_rows = ""
    for s in students:
        table_rows += f"""
        <tr>
            <td>{s['id']}</td>
            <td>{s['name']}</td>
            <td>{s['grade']}</td>
            <td>{s['section']}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>All Students</title>
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: #f8f9fa;
                color: #333;
                text-align: center;
                padding: 40px;
            }}
            h2 {{
                color: #007bff;
                margin-bottom: 30px;
            }}
            table {{
                margin: 0 auto;
                width: 70%;
                border-collapse: collapse;
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 14px;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background: #007bff;
                color: white;
                font-weight: 600;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            a {{
                display: inline-block;
                margin-top: 30px;
                text-decoration: none;
                color: white;
                background: #007bff;
                padding: 10px 20px;
                border-radius: 8px;
                transition: 0.3s;
            }}
            a:hover {{
                background: #0056b3;
            }}
        </style>
    </head>
    <body>
        <h2>📋 Student List</h2>
        <table>
            <tr>
                <th>ID</th><th>Name</th><th>Grade</th><th>Section</th>
            </tr>
            {table_rows}
        </table>
        <a href="/">🏠 Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------------------------
# Get Student by Name (API)
# ---------------------------
@app.route('/student', methods=['GET'])
def get_student():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a student name. Example: /student?name=Gyen"}), 400

    for student in students:
        if student['name'].lower() == name.lower():
            return jsonify({"status": "found", "student": student})

    return jsonify({"status": "not found", "message": f"No student named '{name}' found."}), 404

# ---------------------------
# Add Student (Browser Form)
# ---------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_student_form():
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')

        if not name or not grade or not section:
            return render_template_string("<h3 style='color:red;'>⚠️ All fields are required!</h3><a href='/add'>Back</a>")

        new_id = max(s["id"] for s in students) + 1 if students else 1
        new_student = {"id": new_id, "name": name, "grade": int(grade), "section": section}
        students.append(new_student)
        return redirect(url_for('get_students'))

    html = """
    <html>
    <head>
        <title>Add Student</title>
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                text-align: center;
                padding: 60px;
            }
            form {
                background: white;
                color: #333;
                width: 400px;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            input {
                width: 90%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            button {
                padding: 10px 20px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover {
                background: #218838;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                color: white;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <h2>➕ Add a New Student</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Student Name" required><br>
            <input type="number" name="grade" placeholder="Grade" required><br>
            <input type="text" name="section" placeholder="Section" required><br>
            <button type="submit">Add Student</button>
        </form>
        <a href="/">🏠 Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------------------------
# API: Add Student via JSON
# ---------------------------
@app.route('/student', methods=['POST'])
def add_student_api():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Missing required fields: name, grade, section."}), 400

    new_id = max(student["id"] for student in students) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify({"status": "added", "student": new_student}), 201

# ---------------------------
# Delete Student by ID (API)
# ---------------------------
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student['id'] == id:
            students.remove(student)
            return jsonify({"status": "deleted", "id": id})
    return jsonify({"error": "Student not found"}), 404

# ---------------------------
# Run the App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
