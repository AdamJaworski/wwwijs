function toggleSelectedState(event, org) {
    const items = document.querySelectorAll('.org_button');
    items.forEach(item => item.classList.remove('selected'));

    const element = event.target;
    element.classList.toggle('selected');

    document.getElementById('todo').innerHTML = '';
    document.getElementById('in_progress').innerHTML = '';
    document.getElementById('in_testing').innerHTML = '';
    document.getElementById('finished').innerHTML = '';

    fetch(`/get_tasks?org=${org}`)
        .then(response => response.json())
        .then(data => {
            data.tasks.forEach(task => {
                const taskDiv = document.createElement('div');
                const taskDivHeader = document.createElement('div');
                const taskDivBody = document.createElement('div');
                const taskDivText = document.createElement('p');
                taskDiv.className = 'card mt-3';
                taskDivHeader.className = 'card-header';
                taskDivBody.className = 'card-body';
                taskDivText.className = 'card-text';
                taskDivText.innerText = task.description;
                taskDivHeader.innerText = task.title;
                taskDiv.appendChild(taskDivHeader)
                taskDiv.appendChild(taskDivBody)
                taskDivBody.appendChild(taskDivText)

                switch (task.assigned_to) {
                    case 1:
                        document.getElementById('todo').appendChild(taskDiv);
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