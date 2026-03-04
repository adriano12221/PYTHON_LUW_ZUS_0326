import json

student = {
    "name":"Anna",
    "surname":"Nowak",
    "points":85,
    "city":"Warszawa"
}

try:
    with open("student.json", "w", encoding="utf-8") as f:
        json.dump(student, f, indent=4, ensure_ascii=False)
    print("Plik JSON zapisany")
except IOError as e:
    print(e)
