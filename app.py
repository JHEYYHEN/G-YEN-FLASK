from flask import Flask, jsonify, request, render_template_string

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
# Home Route with Styled HTML
# ---------------------------
@app.route('/')
def home():
    html = """
    <html>
    <head>
      <title>Flask Student API</title>
      <style>
        body {
          font-family: 'Segoe UI', sans-serif;
          background: linear-gradient(135deg, #007bff, #6f42c1);
          color: white;
          text-align: center;
          padding: 60px;
        }
        h1 {
          font-size: 42px;
          margin-bottom: 10px;
        }
        p {
          font-size: 18px;
          margin-bottom: 40px;
        }
        a {
          text-decoration: none;
          background: white;
          color: #007bff;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: bold;
          transition: 0.3s;
        }
        a:hover {
          background: #f8f9fa;
        }
      </style>
    </head>
    <body>
      <h1>🎓 Welcome to the Student API</h1>
      <p>Use this API to manage student records.</p>
      <a href="/students">View All Students</a>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------------------------
# Get All Students
# ---------------------------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "status": "success",
        "count": len(students),
        "data": students
    })

# ---------------------------
# Get a Single Student by Name
# ---------------------------
@app.route('/student', methods=['GET'])
def get_student():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a student name in the URL. Example: /student?name=Gyen"}), 400

    for student in students:
        if student['name'].lower() == name.lower():
            return jsonify({"status": "found", "student": student})

    return jsonify({"status": "not found", "message": f"No student named '{name}' found."}), 404

# ---------------------------
# Add a New Student
# ---------------------------
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Missing required fields (name, grade, section)."}), 400

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
# Delete a Student by ID
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
