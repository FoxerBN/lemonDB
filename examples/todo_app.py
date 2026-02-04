"""
Complete example: Todo Application
A complete working example using all CRUD operations
"""

from app import LemonDB

def show_todos(db):
    """Display all todos"""
    todos = db.findAll()
    print("\n📝 Your Todo List:")
    print("=" * 50)
    if not todos:
        print("  No tasks yet!")
    else:
        for todo in todos:
            status = "✅" if todo['done'] else "⬜"
            print(f"  {status} [{todo['id']}] {todo['task']} ({todo['priority']})")
    print(f"\nTotal: {db.count()} tasks")

def main():
    print("=" * 60)
    print("🍋 LemonDB Todo App")
    print("=" * 60)
    
    # Create database
    schema = {
        "id": {"type": "integer", "required": True, "unique": True},
        "task": {"type": "string", "required": True},
        "priority": "string",
        "done": "boolean"
    }
    
    todos = LemonDB(name="my_todos", schema=schema)
    
    # Test database
    todos.test()
    
    # Add initial tasks
    print("\n--- Adding tasks ---")
    todos.save(
        (1, "Buy groceries", "high", False),
        (2, "Learn Python", "medium", False),
        (3, "Exercise", "high", False),
        (4, "Read a book", "low", False)
    )
    
    show_todos(todos)
    
    # Mark task as done
    print("\n--- Completing task #2 ---")
    todos.updateOne({"id": 2}, {"done": True})
    show_todos(todos)
    
    # Find high priority tasks
    print("\n--- High priority tasks ---")
    high_priority = todos.find({"priority": "high"})
    for task in high_priority:
        print(f"  • {task['task']}")
    
    # Delete completed task
    print("\n--- Removing completed tasks ---")
    completed = todos.find({"done": True})
    for task in completed:
        todos.deleteOne({"id": task['id']})
    
    show_todos(todos)
    
    print("\n✅ Todo app demo completed!")

if __name__ == "__main__":
    main()
