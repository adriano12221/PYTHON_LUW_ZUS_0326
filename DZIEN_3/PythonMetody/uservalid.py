class UserValidator:

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

    @staticmethod
    def validate_age(age):
        return 18<=age<=120

    @staticmethod
    def validate_username(username):
        return len(username)>=3

print(UserValidator.validate_age(10))
print(UserValidator.validate_age(41))
print(UserValidator.validate_age(121))
print(UserValidator.validate_email("test@example.com"))
print(UserValidator.validate_email("test.example.com"))
print(UserValidator.validate_email("test--example.com"))
print(UserValidator.validate_username("Go"))
print(UserValidator.validate_username("Anna"))
print(UserValidator.validate_username("Hieronimususuusususus"))
