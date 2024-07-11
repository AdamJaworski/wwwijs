function updateTasks() {
    document.getElementById('to_do').innerHTML = '';
    document.getElementById('in_progress').innerHTML = '';
    document.getElementById('in_testing').innerHTML = '';
    document.getElementById('finished').innerHTML = '';

    fetch('/get_tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            org: currentOrg
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
            }
        }
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
    document.getElementById('org-table').innerHTML = '';

        fetch('/get_orgs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.status) {
                if(data.redirect) {
                    window.location.href = data.redirect;
                }
            }

            data.orgs.forEach(org => {
                var orgDiv = document.createElement('div');
                orgDiv.className = 'side-panel-active-button';
                orgDiv.id = org.org_name;
                orgDiv.onclick = (event) => toggleSelectedState(event, org.org_name);
                orgDiv.innerText = org.org_name;

                document.getElementById('org-table').appendChild(orgDiv);
            });
        })
        .catch(error => console.error('Error fetching orgs:', error));
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
    .then(response => response.json())
    .then(data => {
        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
            }
        }
        else {
            updateTasks()
        }
    })

    .catch(error => console.error('Error updating task status:', error));
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
    .then(data => {
        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
            }
            if(data.error) {
                console.log(data.error)
            }
        }
        if(data.status){
            closeJoinOrgModal();
            updateOrgs();
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
    .then(response => response.json())
    .then((data) => {
        if(data.status){
            closeJoinOrgModal();
            updateOrgs();
        }
        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
            }
        }
    });
}

function getTaskByID(id) {
    return fetch('/get_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            task_id: id
        })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error fetching task data:', error);
    });
}

function deleteTask(task_id) {
    fetch('/delete_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'task_id': task_id,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            console.log("Deleted Task");
            updateTasks();
            closeTaskModal();
        }
        if (!data.status) {
            if(data.redirect) {
                window.location.href = data.redirect;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}