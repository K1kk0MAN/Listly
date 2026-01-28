document.addEventListener("DOMContentLoaded", () => {
    const listId = document.getElementById("task-wrapper").dataset.listId;
    const addForm = document.getElementById("add-task-form");
    const taskInput = document.getElementById("task-content");
    const tableBody = document.querySelector("table tbody");

    window.toggleTask = itemId => {
        fetch(`/task/toggle/${itemId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            const row = document.querySelector(`tr[data-id="${itemId}"]`);
            const span = row.querySelector("td:nth-child(2) span");

            if (data.checked) {
                span.classList.add("line-through");
            } else {
                span.classList.remove("line-through");
            }
        })
        .catch(error => console.error("Toggle error:", error));
    };

    addForm.addEventListener("submit", e => {
        e.preventDefault();

        const content = taskInput.value.trim();
        if (!content) return;

        fetch(`/tasklist/${listId}/add`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content })
        })
        .then(response => response.json())
        .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const newRow = document.createElement("tr");
        newRow.className = "task-item";
        newRow.setAttribute("data-id", data.id);
        newRow.innerHTML = `
            <td class="text-center">
                <input type="checkbox" class="form-check-input checkbox" onchange="toggleTask(${data.id})">
            </td>
            <td>
                <span class="text-light">${data.content}</span>
            </td>
            <td class="text-light">${new Date().toLocaleDateString()}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-danger" onclick="deleteTask(${data.id})">🗑</button>
            </td>
        `;
        tableBody.prepend(newRow);
        taskInput.value = "";
        })
        .catch(error => console.error("Add error:", error));
    });

    window.deleteTask = itemId => {
        if (!confirm("Are you sure you want to delete this task?")) return;

        fetch(`/task/delete/${itemId}`, {
            method: "POST",
            headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.querySelector(`tr[data-id="${itemId}"]`);
                row.remove();
            } else {
                alert("Failed to delete task.");
            }
        })
        .catch(error => console.error("Delete error:", error));
    };

    function copyList(listId) {
        const button = document.querySelector("#copy-list-btn");
        button.disabled = true;

        fetch(`/copy-list/${listId}/`, {
            method: "POST",
            headers: {
            "X-CSRFToken": getCSRFToken(),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.textContent = "Successfully copied list";
                button.classList.remove("btn-secondary");
                button.classList.add("btn-success");
            } else {
                button.textContent = "Failed to copy list";
                button.classList.add("btn-danger");
            }
        })
        .catch(error => {
            console.error("Copy failed:", error);
            button.textContent = "Error copying list";
            button.classList.add("btn-danger");
        });
    };

    const form = document.getElementById("copy-list-form");
    if (!form) return;

    form.addEventListener("submit", e => {
        e.preventDefault();
        copyList(form.dataset.listId);
    });
});

function copyList(listId) {
    const button = document.querySelector("#copy-list-btn");
    button.disabled = true;

    fetch(`/copy-list/${listId}/`, {
        method: "POST",
        headers: {
        "X-CSRFToken": getCSRFToken(),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.textContent = "Successfully copied list";
            button.classList.remove("btn-secondary");
            button.classList.add("btn-success");
        } else {
            button.textContent = "Failed to copy list";
            button.classList.add("btn-danger");
        }
    })
    .catch(error => {
        console.error("Copy failed:", error);
        button.textContent = "⚠️ Error copying list";
        button.classList.add("btn-danger");
    });
};

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
};
