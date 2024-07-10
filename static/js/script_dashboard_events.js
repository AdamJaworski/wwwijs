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

