# Listly

Listly is a simple web application for creating and managing task lists. I built it using Django on the back end and JavaScript on the front end. My goal was to practice working with models, views, and Ajax calls while also making a clean, mobile-responsive interface. In this README, I explain why I chose each feature and how the code is organized.

## Distinctiveness and Complexity

I chose to build Listly instead of a social network or an online store because I wanted to focus on task management with a few special features. Listly lets users make lists that are either public or private. Public lists can be copied by others with one click. I avoided “likes,” or “comments,” logic so my project stays clearly different from other course examples.

To add complexity, I implemented an “everyday reset” option. If a user turns it on, all tasks in a list automatically uncheck each new day. This meant storing the last reset date in the database and comparing it to the current date whenever the list is viewed. Writing that logic in Django views felt challenging but taught me how to handle date fields and conditional updates.

I also built four JSON endpoints—add, toggle, delete tasks, and copy lists—and connected them to the front end with JavaScript `fetch` calls. This made the app feel fast because actions happen without reloading the page. Coordinating CSRF tokens between Django templates and fetch headers was a good exercise in web security and client-server integration. Overall, mixing Django logic, Ajax, and Bootstrap styling gave the project more depth than a basic example.

## File Explanations

**models.py**  
In this file, I defined three main classes:  
- `User` uses Django’s `AbstractUser` so I can manage user accounts.  
- `List` stores the name, description, owner, public/private setting, and the “everyday_uncheck” variable. It also tracks when it was last reset.  
- `Item` holds each task’s text and whether it is checked.

**views.py**  
This file contains functions for page requests and JSON calls:  
- `index`, `profile`, and `public_lists` render HTML templates with paginated lists.  
- `create_list` and `task_list` let users add new lists and view tasks, including the everyday-reset logic.  
- Four Ajax views—`add_item`, `toggle_item`, `delete_item`, and `copy_list`—send and receive JSON so the page updates smoothly.  
- `login_view`, `register_view`, and `logout_view` manage user authentication.

**urls.py**  
Here I mapped URL paths to each view function. Static files are served automatically during development. This file makes it easy to see every route in one place.

**Templates folder**  
All templates extend from `layout.html`, which loads Bootstrap, a custom dark-theme stylesheet, a favicon, and a responsive navbar. Child templates include:  
- `index.html` (welcome screen)  
- `create.html` (new-list form)  
- `profile.html` (list of user’s lists)  
- `task_list.html` (detailed view of tasks with add/delete/toggle controls)  
- `browse.html` (paginated view of public lists)  
- `login.html` and `register.html` (authentication forms)

**Static folder**  
The static folder holds two key files:  
- `styles.css` defines a dark background, custom form and button styles, and an animated noise effect.  
- `javascript.js` captures DOM events, reads CSRF tokens, and sends `fetch` requests to modify lists and tasks in real time. I wrote it so that adding, checking, or deleting tasks happens immediately on the page.

**static/images**  
This folder provides a small icon in the browser tab.

**requirements.txt**  
This file lists project dependencies, for example:  
```text
Django>=4.0
