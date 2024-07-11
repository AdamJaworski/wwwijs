{
    var currentOrg  = '';
}

function toggleSelectedState(event, org) {
    if (currentOrg == org)
        return
    currentOrg = org
    const items = document.querySelectorAll('.side-panel-active-button');
    items.forEach(item => item.classList.remove('selected'));

    const element = event.target;
    element.classList.toggle('selected');
    document.getElementById('main-sign').innerHTML = `Tablica ${org}`

    updateTasks();
}

function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function openJoinOrgModal(type) {
    if (type == 'create') {
        document.getElementById('join').style.display = 'None';
        document.getElementById('create').style.display = 'block';
    }
    if (type == 'join') {
        document.getElementById('create').style.display = 'None';
        document.getElementById('join').style.display = 'block';
    }
    document.getElementById('joinOrgModal').style.display = 'flex';
}

function closeJoinOrgModal() {
    document.getElementById('joinOrgModal').style.display = 'none';
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = 'none';
}

async function openTaskModal(id) {
    try {
        const data = await getTaskByID(id);

        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
                return;
            }
        }
        const modal_task = document.getElementById('modal-task-content');
        modal_task.className = `modal-task-content prio${data.task.priority}header`;
        document.getElementById('modal-task-title').innerText = data.task.title;
        document.getElementById('modal-task-description').innerText = data.task.description;
        document.getElementById('modal-task-priority').innerText = `\nPriority: ${data.task.priority}`;
        document.getElementById('modal-task-assigned_to').innerText = `Status: ${data.task.assigned_to}`;
        document.getElementById('delete-button').onclick = (event) => deleteTask(data.task.task_id);
        document.getElementById('edit-button').onclick = (event) => editTask(currentOrg, data.task.task_id, data.task.title, data.task.description, data.task.priority, data.task.assigned_to);

        document.getElementById('taskModal').style.display = 'flex';
    } catch (error) {
        console.error('Error opening task modal:', error);
    }
}


function editTask(org, task_id, title, description, priority, assigned_to) {
    const encodedOrg = encodeURIComponent(org);
    const encodedTitle = encodeURIComponent(title);
    const encodedDescription = encodeURIComponent(description);
    const encodedPriority = encodeURIComponent(priority);
    const encodedAssignedTo = encodeURIComponent(assigned_to);

    const url = `/create_new_issue?task_id=${task_id}&org=${encodedOrg}&title=${encodedTitle}&description=${encodedDescription}&priority=${encodedPriority}&assigned_to=${encodedAssignedTo}`;

    console.log(url);
    href_js(url);
}