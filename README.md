# Listly

Listly is a lightweight Django web application designed to help users organize their daily tasks and to-do lists efficiently. It provides a clean, intuitive interface for creating, managing, and tracking tasks with features like public/private lists, everyday automatic resets, and one-click list copying. The application is built with a focus on simplicity, user experience, and practical functionality.

The tool is intended to be easy to use, mobile-responsive, and suitable both for personal task management and as a learning project demonstrating Django web development, Ajax integration, and modern web design.

---

## Overview

Listly automates task management using the following workflow:

1. Users create custom task lists with names and descriptions
2. Lists can be set as public (shareable) or private (personal)
3. Tasks are added to lists with simple text entries
4. Tasks can be checked/unchecked to track completion
5. Optional "everyday reset" feature automatically unchecks all tasks daily
6. Public lists can be copied by other users with one click
7. All actions happen in real-time without page reloads using Ajax

The application uses Django's authentication system to ensure each user has their own secure workspace while allowing optional collaboration through public lists.

---

## Features

- **User Authentication**: Secure login and registration system
- **Multiple List Management**: Create unlimited task lists with custom names and descriptions
- **Public & Private Lists**: Control visibility and sharing of your lists
- **Everyday Reset Option**: Automatically uncheck all tasks at the start of each day
- **One-Click List Copying**: Copy public lists created by other users instantly
- **Real-Time Updates**: Add, toggle, and delete tasks without page reloads
- **Mobile-Responsive Design**: Clean interface that works on all devices
- **Dark Theme Interface**: Modern, eye-friendly design with animated background
- **Pagination**: Browse public lists efficiently with paginated views
- **No External Dependencies**: Uses only Django and standard web technologies

---

## Installation

### Prerequisites

- Python 3.7 or newer
- Django 4.0 or newer
- Standard Python libraries only (no complex external dependencies)

### Clone the Repository

```bash
git clone https://github.com/K1kk0MAN/Listly.git
cd Listly
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

---

## Usage

### Creating Your First List

1. Register for an account or log in if you already have one
2. Navigate to your profile page
3. Click "Create New List"
4. Enter a list name and optional description
5. Choose whether to make the list public or private
6. Optionally enable "Everyday Reset" to automatically uncheck tasks daily
7. Click "Create" to save your list

### Managing Tasks

Once you've created a list, you can:

- **Add tasks**: Enter task text in the input field and click "Add"
- **Check/uncheck tasks**: Click the checkbox next to any task to toggle completion
- **Delete tasks**: Click the delete button (×) to remove a task
- **View progress**: See completed vs. total tasks at the top of the list

All task actions happen instantly using Ajax—no page refresh required.

### Browsing and Copying Public Lists

1. Navigate to "Browse Public Lists" from the navigation menu
2. View lists created by other users
3. Click "Copy List" on any public list to add it to your account
4. The copied list will appear in your profile with all its tasks
5. You can then modify, delete, or customize the copied list

### Everyday Reset Feature

When enabled, the "everyday reset" feature:
- Automatically unchecks all tasks in the list at midnight each day
- Helps maintain daily task routines
- Perfect for recurring checklists (morning routines, daily work tasks, etc.)
- The reset happens automatically when you view the list after a new day begins

---

## Project Structure

### Django Apps

**tasks/** - Main application containing all functionality

### Key Files

**models.py**
- `User`: Extends Django's AbstractUser for authentication
- `List`: Stores list information (name, description, owner, public status, everyday reset)
- `Item`: Represents individual tasks with text and completion status

**views.py**
- `index`: Landing page view
- `profile`: User's personal list dashboard
- `create_list`: Form for creating new lists
- `task_list`: Detailed view of tasks with everyday-reset logic
- `public_lists`: Paginated browse view of public lists
- `add_item`: Ajax endpoint for adding tasks
- `toggle_item`: Ajax endpoint for checking/unchecking tasks
- `delete_item`: Ajax endpoint for deleting tasks
- `copy_list`: Ajax endpoint for copying public lists
- `login_view`, `register_view`, `logout_view`: Authentication views

**urls.py**
- Maps URL patterns to view functions
- Includes routes for all pages and Ajax endpoints

**templates/**
- `layout.html`: Base template with Bootstrap, navbar, and styling
- `index.html`: Welcome/landing page
- `create.html`: List creation form
- `profile.html`: User's list management dashboard
- `task_list.html`: Detailed task view with interactive controls
- `browse.html`: Public lists browser with pagination
- `login.html` and `register.html`: Authentication forms

**static/**
- `styles.css`: Custom dark theme styling and animations
- `javascript.js`: Ajax functionality for real-time task management
- `images/`: Application icons and assets

**requirements.txt**
- Lists all Python dependencies

---

## Technical Implementation

### Front-End Architecture

The application uses vanilla JavaScript with the Fetch API to communicate with Django's backend. CSRF tokens are properly handled for all POST requests. The interface is built with Bootstrap 5 for responsive design, with custom CSS providing the dark theme and visual polish.

### Back-End Architecture

Django handles all server-side logic, including:
- User authentication and session management
- Database operations using Django ORM
- JSON API endpoints for Ajax requests
- Template rendering for initial page loads
- Date-based logic for everyday resets

### Database Schema

The SQLite database (included for development) contains three main tables:
- **Users**: Authentication and account information
- **Lists**: Task list metadata and settings
- **Items**: Individual tasks linked to lists

### Everyday Reset Implementation

The reset feature works by:
1. Storing `last_reset` timestamp in the List model
2. Comparing `last_reset` to current date when list is viewed
3. If different days, unchecking all tasks and updating `last_reset`
4. This ensures resets happen once per day, only when needed

### Security Features

- Django's built-in CSRF protection on all forms
- Password hashing for user authentication
- Login required decorators on protected views
- User ownership validation before allowing list modifications

---

## API Endpoints

Listly provides several JSON endpoints for Ajax operations:

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `/add-item/<list_id>` | POST | Add new task to list | JSON with item data |
| `/toggle-item/<item_id>` | POST | Toggle task completion | JSON with updated status |
| `/delete-item/<item_id>` | POST | Remove task from list | JSON success message |
| `/copy-list/<list_id>` | POST | Copy public list to user's account | JSON with new list ID |

All endpoints require authentication and return appropriate error messages if validation fails.

---

## Distinctiveness and Complexity

### What Makes Listly Different

**Beyond Basic CRUD**: While Listly includes standard create, read, update, and delete operations, it goes further with:
- The everyday reset feature requiring date-comparison logic
- Public/private list distinction with copy functionality
- Real-time interface updates using Ajax and JSON
- Mobile-first responsive design with custom styling

**Not a Social Network**: Unlike typical social platforms, Listly focuses on task management with optional sharing rather than social interactions. There are no likes, comments, followers, or feeds.

**Not an E-commerce Site**: The application has no concept of products, shopping carts, payments, or inventory—it's purely about organizing personal tasks.

### Technical Complexity

The project demonstrates:
- Full-stack development with Django backend and JavaScript frontend
- RESTful API design with JSON endpoints
- CSRF-protected Ajax operations
- Date-based automatic task resets
- User authentication and authorization
- Responsive design using Bootstrap framework
- Custom CSS animations and styling
- Database relationship management (one-to-many, foreign keys)
- Pagination for large datasets
- Template inheritance and Django templating language

---

## Mobile Responsiveness

Listly is fully responsive and optimized for:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

The Bootstrap grid system ensures proper layout across all screen sizes, and the interface adapts automatically without losing functionality.

---

## Future Enhancements

Potential features for future versions:
- Task priorities and due dates
- Collaborative lists with multiple users
- Task categories or tags
- Search and filter functionality
- Export lists to CSV or PDF
- Drag-and-drop task reordering
- Dark/light theme toggle
- Email notifications for shared lists
- Task completion statistics

---

## Testing

The application has been tested with:
- User registration and login flows
- List creation with various settings
- Task addition, completion, and deletion
- Public list browsing and copying
- Everyday reset functionality
- Mobile device compatibility
- CSRF protection validation

To run manual tests:
1. Create an account
2. Create multiple lists with different settings
3. Add and manage tasks in various lists
4. Test the everyday reset by changing system date
5. Create public lists and copy them with another account

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## Acknowledgments

- Built with Django web framework
- Styled with Bootstrap 5
- Inspired by the need for simple, effective task management
- Created as a final project demonstrating web development skills

---
