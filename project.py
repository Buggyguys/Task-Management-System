class Project:
    def __init__(self, pid, name, description, deadline, assigned_users=None):
        self.pid = pid
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assigned_users = assigned_users or []

    def to_dict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline,
            "assigned_users": self.assigned_users,
        }

    @staticmethod
    def from_dict(data):
        return Project(
            data["pid"],
            data["name"],
            data["description"],
            data["deadline"],
            data["assigned_users"],
        )
