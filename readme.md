# Simple To-Do List

## Environment
Python (3.6.5), Django (3.0)

## Other Libraries
python-dateutil (2.8.0)

## Usage
### Task List
You can:

- view all tasks;
- jump to edit page; and
- delete tasks.

### Create / Edit Task
Fill out the fields below and submit.

- Task name
- Deadline
- Priority (Low, Medium, High or Urgent)
- Repeat (Check if the task is periodical)
  - Interval (1 week, 2 weeks, 1 month, 2 months or custom)
  - Custom Duration (if you selected custom interval)
- Parent Task

If deadline of periodical task has passed, the deadline will be automatically refreshed.

### Delete Task

If you delete a task which has children tasks, those children will be also deleted.
