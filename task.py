class Task:
    def __init__(self, tid, name, description, priority, status, project_id, user_id=None):
        self.tid = tid
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.project_id = project_id
        self.user_id = user_id

    def to_dict(self):
        return {
            "tid": self.tid,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "project_id": self.project_id,
            "user_id": self.user_id,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["tid"],
            data["name"],
            data["description"],
            data["priority"],
            data["status"],
            data["project_id"],
            data.get("user_id"),  # Handle missing `user_id` gracefully
        )
