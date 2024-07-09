{
    var currentOrg  = '';
}

function toggleSelectedState(event, org) {
    if (currentOrg == org)
        return
    currentOrg = org
    const items = document.querySelectorAll('.org_button');
    items.forEach(item => item.classList.remove('selected'));

    const element = event.target;
    element.classList.toggle('selected');

    updateTasks();
}

function updateTasks() {
    document.getElementById('to_do').innerHTML = '';
    document.getElementById('in_progress').innerHTML = '';
    document.getElementById('in_testing').innerHTML = '';
    document.getElementById('finished').innerHTML = '';


    fetch(`/get_tasks?org=${currentOrg}`)
        .then(response => response.json())
        .then(data => {
            data.tasks.forEach(task => {
                const taskDiv = document.createElement('div');
                taskDiv.onclick = (event) => openTaskModal(task.task_id);
                taskDiv.className = 'card mt-3';
                taskDiv.setAttribute('draggable', true);
                taskDiv.setAttribute('ondragstart', 'drag(event)');
                taskDiv.setAttribute('id', `task-${task.task_id}`);

                const taskDivHeader = document.createElement('div');
                const taskDivBody = document.createElement('div');
                const taskDivText = document.createElement('p');

                taskDivHeader.className = `card-header prio${task.priority}header`;
                taskDivBody.className = `card-body  prio${task.priority}body`;
                taskDivText.className = 'card-text';

                short_description = task.description.split('.')[0];
                taskDivText.innerText = short_description + '...';
                taskDivHeader.innerText = task.title;

                taskDiv.appendChild(taskDivHeader);
                taskDiv.appendChild(taskDivBody);
                taskDivBody.appendChild(taskDivText);

                switch (task.assigned_to) {
                    case 1:
                        document.getElementById('to_do').appendChild(taskDiv);
                        break;
                    case 2:
                        document.getElementById('in_progress').appendChild(taskDiv);
                        break;
                    case 3:
                        document.getElementById('in_testing').appendChild(taskDiv);
                        break;
                    case 4:
                        document.getElementById('finished').appendChild(taskDiv);
                        break;
                    default:
                        break;
                }
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));
}

function updateOrgs() {
    document.getElementById('org_table').innerHTML = '';

    fetch(`/get_orgs`)
        .then(response => response.json())
        .then(data => {
            data.orgs.forEach(org => {
                var orgDiv = document.createElement('div');
                orgDiv.className = 'org_button';
                orgDiv.id = org;
                orgDiv.onclick = (event) => toggleSelectedState(event, org);
                orgDiv.innerText = org;

                document.getElementById('org_table').appendChild(orgDiv);
            });
        })
        .catch(error => console.error('Error fetching orgs:', error));
}

function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
    event.preventDefault();
    const data = event.dataTransfer.getData("text");

    const newStatus = event.target.id;
    fetch(`/update_task_status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            task_id: data.replace('task-', ''),
            new_status: newStatus
        })
    })
    .then(response => {
            response.json();
            updateTasks()
        })

    .catch(error => console.error('Error updating task status:', error));
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

function submitJoinOrgForm(event) {
    const orgName = document.getElementById('orgName').value;
    const orgPassword = document.getElementById('orgPassword').value;

    if (orgName == '' || orgPassword == '') {
        return
    }

    fetch('/join_org', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            orgName: orgName,
            orgPassword: orgPassword
        })
    })
    .then((response) => response.json())
    .then((json) => {
        if(json.status){
            console.log("Added org");
            closeJoinOrgModal();
            updateOrgs();
        }
        else{
            console.log(json.error)
        }
    });
}

function submitCreateOrgForm(event) {
    const orgName = document.getElementById('orgName').value;
    const orgPassword = document.getElementById('orgPassword').value;

    if (orgName == '' || orgPassword == '') {
        return
    }

    fetch('/create_org', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            orgName: orgName,
            orgPassword: orgPassword
        })
    })
    .then((response) => response.json())
    .then((json) => {
        if(json.status){
            console.log(json.msg);
            closeJoinOrgModal();
            updateOrgs();
        }
        else{
            console.log(json.error)
        }
    });
}

function openTaskModal(id) {
    fetch(`/get_task?task_id=${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.task) {
                throw new Error('Task data is missing');
            }
            console.log('Task data:', data.task);
            modal_task = document.getElementById('modal-task-content');
            modal_task.className = `modal-task-content prio${data.task.priority}header`;
            document.getElementById('modal-task-title').innerText = data.task.title;
            document.getElementById('modal-task-description').innerText = data.task.description;
            document.getElementById('modal-task-priority').innerText = `\nPriority: ${data.task.priority}`;
            document.getElementById('modal-task-assigned_to').innerText = `Status: ${data.task.assigned_to}`;
        })
        .catch(error => {
            console.error('Error fetching task data:', error);
        });
    document.getElementById('taskModal').style.display = 'flex';
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = 'none';
}