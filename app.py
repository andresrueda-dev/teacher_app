def add_student(user, name):
    db.collection("students").add({
        "user": user,
        "name": name,
        "points": 0
    })


def get_students(user):
    docs = db.collection("students").where("user", "==", user).stream()
    
    students = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        students.append(data)
    
    return students


def add_points(student_id, points):
    db.collection("students").document(student_id).update({
        "points": firestore.Increment(points)
    })


def login_user(username, password):
    if username == "admin" and password == "1234":
        return True, "ok"
    else:
        return False, "Invalid credentials"
