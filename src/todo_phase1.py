"""
Phase I - In-Memory Todo CLI Application

A simple, single-user console application for task management with in-memory storage.
Features: Add, View, Update, Delete, and Mark tasks as Complete/Incomplete.

Constitutional Compliance:
- Python standard library only (no external dependencies)
- In-memory storage only (no persistence)
- Single file architecture with clean separation of concerns
- Clean architecture: Data Layer, Presentation Layer, Control Flow
"""

# ============================================================================
# DATA LAYER - Task Storage and CRUD Operations
# ============================================================================

# Global task storage
tasks = []
next_id = 1


def add_task(description):
    """
    Create a new task with auto-generated ID and append to task list.

    Args:
        description (str): Task description (already validated and trimmed)

    Returns:
        int: ID of the newly created task
    """
    global next_id
    task = {
        'id': next_id,
        'description': description,
        'completed': False
    }
    tasks.append(task)
    task_id = next_id
    next_id += 1
    return task_id


def get_all_tasks():
    """
    Return a copy of all tasks.

    Returns:
        list: Copy of the task list
    """
    return tasks.copy()


def find_task_by_id(task_id):
    """
    Find and return a task by its ID.

    Args:
        task_id (int): Task ID to search for

    Returns:
        dict or None: Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None


def update_task(task_id, new_description):
    """
    Update the description of an existing task.

    Args:
        task_id (int): ID of task to update
        new_description (str): New description (already validated and trimmed)

    Returns:
        bool: True if task was updated, False if task not found
    """
    task = find_task_by_id(task_id)
    if task is None:
        return False
    task['description'] = new_description
    return True


def delete_task(task_id):
    """
    Delete a task from the task list.

    Args:
        task_id (int): ID of task to delete

    Returns:
        bool: True if task was deleted, False if task not found
    """
    task = find_task_by_id(task_id)
    if task is None:
        return False
    tasks.remove(task)
    return True


def toggle_task_status(task_id):
    """
    Toggle the completion status of a task.

    Args:
        task_id (int): ID of task to toggle

    Returns:
        bool or None: New status (True/False) if successful, None if task not found
    """
    task = find_task_by_id(task_id)
    if task is None:
        return None
    task['completed'] = not task['completed']
    return task['completed']


# ============================================================================
# PRESENTATION LAYER - CLI Interface and User Interaction
# ============================================================================

def display_main_menu():
    """Display the main menu with all available options."""
    print("\n" + "=" * 40)
    print("=== Todo Application - Phase I ===")
    print("=" * 40)
    print("\nMain Menu:")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark task as complete/incomplete")
    print("6. Exit")
    print()


def get_menu_choice():
    """
    Get and validate menu choice from user.

    Returns:
        int: Valid menu choice (1-6)
    """
    while True:
        try:
            choice_input = input("Enter your choice (1-6): ").strip()
            choice = int(choice_input)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Error: Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Error: Invalid choice. Please enter a number between 1 and 6.")


def get_task_description():
    """
    Get and validate task description from user.

    Returns:
        str or None: Trimmed description if valid, None if empty
    """
    description = input("Enter task description: ").strip()
    if not description:
        print("Error: Task description cannot be empty")
        return None
    return description


def get_task_id(prompt_message):
    """
    Get and validate task ID from user.

    Args:
        prompt_message (str): Prompt to display to user

    Returns:
        int or None: Task ID if valid integer, None if invalid
    """
    try:
        id_input = input(prompt_message).strip()
        task_id = int(id_input)
        return task_id
    except ValueError:
        print("Error: Invalid task ID. Please enter a number")
        return None


def display_task_list():
    """Display all tasks in a formatted list or empty message."""
    all_tasks = get_all_tasks()

    if not all_tasks:
        print("\nNo tasks found. Your list is empty.")
        return

    print("\n" + "=" * 40)
    print("=== Your Tasks ===")
    print("=" * 40)

    complete_count = 0
    incomplete_count = 0

    for task in all_tasks:
        status = "[X]" if task['completed'] else "[ ]"
        print(f"{task['id']}. {status} {task['description']}")

        if task['completed']:
            complete_count += 1
        else:
            incomplete_count += 1

    total = len(all_tasks)
    print(f"\nTotal: {total} tasks ({complete_count} complete, {incomplete_count} incomplete)")


def display_confirmation(message):
    """
    Display a confirmation message.

    Args:
        message (str): Confirmation message to display
    """
    print(message)


def display_error(message):
    """
    Display an error message.

    Args:
        message (str): Error message to display
    """
    if not message.startswith("Error:"):
        message = f"Error: {message}"
    print(message)


# ============================================================================
# CONTROL FLOW - Menu Handlers and Main Loop
# ============================================================================

def handle_add_task():
    """Handle the 'Add Task' menu option."""
    description = get_task_description()
    if description is not None:
        task_id = add_task(description)
        display_confirmation(f"Task added successfully with ID {task_id}")


def handle_view_tasks():
    """Handle the 'View All Tasks' menu option."""
    display_task_list()


def handle_update_task():
    """Handle the 'Update Task' menu option."""
    task_id = get_task_id("Enter task ID to update: ")
    if task_id is None:
        return

    task = find_task_by_id(task_id)
    if task is None:
        display_error(f"Task with ID {task_id} not found")
        return

    new_description = get_task_description()
    if new_description is None:
        return

    if update_task(task_id, new_description):
        display_confirmation(f"Task {task_id} updated successfully")


def handle_delete_task():
    """Handle the 'Delete Task' menu option."""
    task_id = get_task_id("Enter task ID to delete: ")
    if task_id is None:
        return

    if delete_task(task_id):
        display_confirmation(f"Task {task_id} deleted successfully")
    else:
        display_error(f"Task with ID {task_id} not found")


def handle_toggle_status():
    """Handle the 'Toggle Task Status' menu option."""
    task_id = get_task_id("Enter task ID to toggle status: ")
    if task_id is None:
        return

    new_status = toggle_task_status(task_id)
    if new_status is None:
        display_error(f"Task with ID {task_id} not found")
    else:
        status_text = "complete" if new_status else "incomplete"
        display_confirmation(f"Task {task_id} marked as {status_text}")


def handle_exit():
    """Handle the 'Exit' menu option."""
    print("\nThank you for using Todo Application. Goodbye!")
    return True


def main():
    """Main application loop."""
    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice == 1:
            handle_add_task()
        elif choice == 2:
            handle_view_tasks()
        elif choice == 3:
            handle_update_task()
        elif choice == 4:
            handle_delete_task()
        elif choice == 5:
            handle_toggle_status()
        elif choice == 6:
            if handle_exit():
                break


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
