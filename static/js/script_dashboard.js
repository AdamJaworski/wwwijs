{
    var currentOrg = '';
}

function toggleSelectedState(event, org) {
    const items = document.querySelectorAll('.org_button');
    items.forEach(item => item.classList.remove('selected'));

    const element = event.target;
    element.classList.toggle('selected');

    currentOrg = org;
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
                taskDiv.className = 'card mt-3';
                taskDiv.setAttribute('draggable', true);
                taskDiv.setAttribute('ondragstart', 'drag(event)');
                taskDiv.setAttribute('id', `task-${task.task_id}`);

                const taskDivHeader = document.createElement('div');
                const taskDivBody = document.createElement('div');
                const taskDivText = document.createElement('p');

                taskDivHeader.className = 'card-header';
                taskDivBody.className = 'card-body';
                taskDivText.className = 'card-text';

                taskDivText.innerText = task.description;
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
    .then(response => response.json())
    .then(data => {
        console.log('Task status updated:', data);
    })
    .catch(error => console.error('Error updating task status:', error));

    updateTasks();
}