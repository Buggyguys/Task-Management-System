class User:
    def __init__(self, uid, first_name, last_name, email):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.projects = []

    def to_dict(self):
        return {
            "uid": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects],
        }

    @staticmethod
    def from_dict(data):
        user = User(data["uid"], data["first_name"], data["last_name"], data["email"])
        return user
