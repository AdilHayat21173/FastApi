from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict

# Create FastAPI app
app = FastAPI(title="Student Admission API")

# Student model
class Student(BaseModel):
    name: str
    father_name: str
    age: int
    class_name: str

# In-memory "database"
students: Dict[int, Student] = {}

# HTML Frontend
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Admission Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .main-content {
            padding: 30px;
        }

        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }

        .tab-button {
            padding: 15px 30px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }

        .tab-button.active {
            color: #4facfe;
            border-bottom-color: #4facfe;
            font-weight: 600;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #4facfe;
        }

        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-right: 10px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
        }

        .btn-secondary {
            background: #f8f9fa;
            color: #666;
            border: 2px solid #e1e5e9;
        }

        .btn-secondary:hover {
            background: #e9ecef;
        }

        .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
        }

        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .search-box input {
            flex: 1;
        }

        .student-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #4facfe;
            transition: transform 0.3s ease;
        }

        .student-card:hover {
            transform: translateX(5px);
        }

        .student-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }

        .info-item {
            display: flex;
            flex-direction: column;
        }

        .info-label {
            font-weight: 600;
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .info-value {
            font-size: 16px;
            color: #333;
        }

        .student-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
        }

        .message.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .message.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4facfe;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media (max-width: 768px) {
            .tabs {
                flex-wrap: wrap;
            }
            
            .tab-button {
                flex: 1;
                min-width: 120px;
            }
            
            .two-column {
                grid-template-columns: 1fr;
            }
            
            .search-box {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Student Admission Management</h1>
            <p>Manage student records with ease</p>
        </div>
        
        <div class="main-content">
            <div class="tabs">
                <button class="tab-button active" onclick="showTab('add')">➕ Add Student</button>
                <button class="tab-button" onclick="showTab('search')">🔍 Search Students</button>
                <button class="tab-button" onclick="showTab('all')">📋 All Students</button>
            </div>

            <div id="add" class="tab-content active">
                <h2>Add New Student</h2>
                <div id="add-message"></div>
                <form id="addStudentForm" class="two-column">
                    <div class="form-group">
                        <label for="add-student-id">Student ID:</label>
                        <input type="number" id="add-student-id" required min="1">
                    </div>
                    <div class="form-group">
                        <label for="add-name">Name:</label>
                        <input type="text" id="add-name" required>
                    </div>
                    <div class="form-group">
                        <label for="add-father-name">Father's Name:</label>
                        <input type="text" id="add-father-name" required>
                    </div>
                    <div class="form-group">
                        <label for="add-age">Age:</label>
                        <input type="number" id="add-age" required min="1" max="100">
                    </div>
                    <div class="form-group">
                        <label for="add-class">Class:</label>
                        <input type="text" id="add-class" required placeholder="e.g., 10th Grade, BSc Computer Science">
                    </div>
                    <div></div>
                </form>
                <button type="submit" form="addStudentForm" class="btn btn-primary">Add Student</button>
                <button type="button" class="btn btn-secondary" onclick="clearForm('add')">Clear Form</button>
            </div>

            <div id="search" class="tab-content">
                <h2>Search Students</h2>
                <div class="search-box">
                    <input type="number" id="search-id" placeholder="Search by Student ID">
                    <button class="btn btn-primary" onclick="searchById()">Search by ID</button>
                </div>
                <div class="search-box">
                    <input type="text" id="search-name" placeholder="Search by Name">
                    <button class="btn btn-primary" onclick="searchByName()">Search by Name</button>
                </div>
                <div id="search-results"></div>
            </div>

            <div id="all" class="tab-content">
                <h2>All Students</h2>
                <button class="btn btn-primary" onclick="loadAllStudents()">🔄 Refresh List</button>
                <div id="all-students"></div>
            </div>
        </div>
    </div>

    <!-- Update Student Form -->
    <div id="updateForm" style="display: none;" class="tab-content">
        <h2>Update Student</h2>
        <div id="update-message"></div>
        <form id="updateStudentForm" class="two-column">
            <input type="hidden" id="update-student-id">
            <div class="form-group">
                <label for="update-name">Name:</label>
                <input type="text" id="update-name" required>
            </div>
            <div class="form-group">
                <label for="update-father-name">Father's Name:</label>
                <input type="text" id="update-father-name" required>
            </div>
            <div class="form-group">
                <label for="update-age">Age:</label>
                <input type="number" id="update-age" required min="1" max="100">
            </div>
            <div class="form-group">
                <label for="update-class">Class:</label>
                <input type="text" id="update-class" required>
            </div>
        </form>
        <button type="submit" form="updateStudentForm" class="btn btn-primary">Update Student</button>
        <button type="button" class="btn btn-secondary" onclick="cancelUpdate()">Cancel</button>
    </div>

    <script>
        // Global variables
        let studentsData = {};
        
        // Get the current origin for API calls
        const API_BASE = window.location.origin;

        function showMessage(elementId, message, type = 'success') {
            const element = document.getElementById(elementId);
            element.innerHTML = `<div class="message ${type}">${message}</div>`;
            setTimeout(() => {
                element.innerHTML = '';
            }, 5000);
        }

        function showLoading(elementId) {
            const element = document.getElementById(elementId);
            element.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    Loading...
                </div>
            `;
        }

        // Tab management
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'all') {
                loadAllStudents();
            }
        }

        // Add student
        document.getElementById('addStudentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const studentData = {
                name: document.getElementById('add-name').value,
                father_name: document.getElementById('add-father-name').value,
                age: parseInt(document.getElementById('add-age').value),
                class_name: document.getElementById('add-class').value
            };
            
            const studentId = parseInt(document.getElementById('add-student-id').value);
            
            try {
                const response = await fetch(`${API_BASE}/students/${studentId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(studentData)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    showMessage('add-message', 'Student added successfully!', 'success');
                    clearForm('add');
                    studentsData[studentId] = studentData;
                } else {
                    const error = await response.json();
                    showMessage('add-message', `Error: ${error.detail}`, 'error');
                }
            } catch (error) {
                showMessage('add-message', `Network error: ${error.message}`, 'error');
            }
        });

        // Search by ID
        async function searchById() {
            const studentId = document.getElementById('search-id').value;
            if (!studentId) return;
            
            showLoading('search-results');
            
            try {
                const response = await fetch(`${API_BASE}/students/${studentId}`);
                
                if (response.ok) {
                    const student = await response.json();
                    displayStudents('search-results', [{ id: studentId, ...student }]);
                } else {
                    const error = await response.json();
                    document.getElementById('search-results').innerHTML = `<div class="message error">Student not found</div>`;
                }
            } catch (error) {
                document.getElementById('search-results').innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
            }
        }

        // Search by name
        async function searchByName() {
            const name = document.getElementById('search-name').value;
            if (!name) return;
            
            showLoading('search-results');
            
            try {
                const response = await fetch(`${API_BASE}/students/by-name/${encodeURIComponent(name)}`);
                
                if (response.ok) {
                    const students = await response.json();
                    displayStudents('search-results', students.map((student, index) => ({ id: 'N/A', ...student })));
                } else {
                    const error = await response.json();
                    document.getElementById('search-results').innerHTML = `<div class="message error">No students found with that name</div>`;
                }
            } catch (error) {
                document.getElementById('search-results').innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
            }
        }

        // Load all students - show the current in-memory students
        async function loadAllStudents() {
            const container = document.getElementById('all-students');
            
            if (Object.keys(studentsData).length === 0) {
                container.innerHTML = `
                    <div class="message error">
                        No students found. Add some students first using the "Add Student" tab.
                    </div>
                `;
                return;
            }
            
            const students = Object.keys(studentsData).map(id => ({
                id: id,
                ...studentsData[id]
            }));
            
            displayStudents('all-students', students);
        }

        // Display students
        function displayStudents(containerId, students) {
            const container = document.getElementById(containerId);
            
            if (!students || students.length === 0) {
                container.innerHTML = '<div class="message error">No students found</div>';
                return;
            }
            
            const studentsHtml = students.map(student => `
                <div class="student-card">
                    <div class="student-info">
                        <div class="info-item">
                            <span class="info-label">Student ID</span>
                            <span class="info-value">${student.id}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Name</span>
                            <span class="info-value">${student.name}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Father's Name</span>
                            <span class="info-value">${student.father_name}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Age</span>
                            <span class="info-value">${student.age} years</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Class</span>
                            <span class="info-value">${student.class_name}</span>
                        </div>
                    </div>
                    ${student.id !== 'N/A' ? `
                        <div class="student-actions">
                            <button class="btn btn-secondary" onclick="editStudent(${student.id}, '${student.name}', '${student.father_name}', ${student.age}, '${student.class_name}')">✏️ Edit</button>
                            <button class="btn btn-danger" onclick="deleteStudent(${student.id})">🗑️ Delete</button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
            
            container.innerHTML = studentsHtml;
        }

        // Edit student
        function editStudent(id, name, fatherName, age, className) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById('updateForm').style.display = 'block';
            document.getElementById('updateForm').classList.add('active');
            
            document.getElementById('update-student-id').value = id;
            document.getElementById('update-name').value = name;
            document.getElementById('update-father-name').value = fatherName;
            document.getElementById('update-age').value = age;
            document.getElementById('update-class').value = className;
        }

        // Update student form submission
        document.getElementById('updateStudentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const studentId = document.getElementById('update-student-id').value;
            const studentData = {
                name: document.getElementById('update-name').value,
                father_name: document.getElementById('update-father-name').value,
                age: parseInt(document.getElementById('update-age').value),
                class_name: document.getElementById('update-class').value
            };
            
            try {
                const response = await fetch(`${API_BASE}/students/${studentId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(studentData)
                });
                
                if (response.ok) {
                    showMessage('update-message', 'Student updated successfully!', 'success');
                    studentsData[studentId] = studentData;
                    setTimeout(() => {
                        cancelUpdate();
                        showTab('search');
                    }, 1500);
                } else {
                    const error = await response.json();
                    showMessage('update-message', `Error: ${error.detail}`, 'error');
                }
            } catch (error) {
                showMessage('update-message', `Network error: ${error.message}`, 'error');
            }
        });

        // Cancel update
        function cancelUpdate() {
            document.getElementById('updateForm').style.display = 'none';
            document.getElementById('updateForm').classList.remove('active');
            showTab('search');
        }

        // Delete student
        async function deleteStudent(studentId) {
            if (!confirm('Are you sure you want to delete this student?')) {
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/students/${studentId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    alert('Student deleted successfully!');
                    delete studentsData[studentId];
                    loadAllStudents();
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.detail}`);
                }
            } catch (error) {
                alert(`Network error: ${error.message}`);
            }
        }

        // Clear form
        function clearForm(formPrefix) {
            document.getElementById(`${formPrefix}-student-id`).value = '';
            document.getElementById(`${formPrefix}-name`).value = '';
            document.getElementById(`${formPrefix}-father-name`).value = '';
            document.getElementById(`${formPrefix}-age`).value = '';
            document.getElementById(`${formPrefix}-class`).value = '';
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('add-student-id').focus();
        });
    </script>
</body>
</html>
"""

# Route to serve the HTML frontend
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return HTMLResponse(content=html_content, status_code=200)

# API Routes (same as before)

# CREATE - Add new student
@app.post("/students/{student_id}")
def add_student(student_id: int, student: Student):
    if student_id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students[student_id] = student
    return {"message": "Student added successfully", "student": student}

# READ - Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

# READ - Get student(s) by name
@app.get("/students/by-name/{name}")
def get_student_by_name(name: str):
    result = [student for student in students.values() if student.name.lower() == name.lower()]
    if not result:
        raise HTTPException(status_code=404, detail="No student found with that name")
    return result

# UPDATE - Update student details
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student
    return {"message": "Student updated successfully", "student": student}

# DELETE - Remove student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted successfully"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)