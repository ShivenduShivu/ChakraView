class ValidationError(Exception):
    """Base validation error for all task validation failures."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TaskNotFoundError(ValidationError):
    """Raised when a task name does not exist in the registry."""
    def __init__(self, task_name: str):
        self.task_name = task_name
        super().__init__(f"Task '{task_name}' not found in registry.")


class MissingInputError(ValidationError):
    """Raised when a required input field is missing from the task input."""
    def __init__(self, task_name: str, missing_field: str):
        self.task_name = task_name
        self.missing_field = missing_field
        super().__init__(
            f"Task '{task_name}' missing required input '{missing_field}'."
        )


class InvalidInputError(ValidationError):
    """Raised when the input field is not a dictionary."""
    def __init__(self, task_name: str):
        self.task_name = task_name
        super().__init__(
            f"Task '{task_name}' has invalid input type: expected a dict."
        )
