function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const queries = queryString.split("&");

    queries.forEach(query => {
        const [key, value] = query.split("=");
        params[key] = decodeURIComponent(value);
    });

    if(params.task_id){
        console.log(params);
        document.getElementById('form').action = `/update_task?taskid=${params.task_id}`;
        document.getElementById('title').value = params.title;
        document.getElementById('description').value = params.description;
        document.getElementById('priority').value = params.priority;
        switch (params.assigned_to) {
            case 'To Do':
                document.getElementById('status').value = 1;
                break;
            case "In Progress":
                document.getElementById('status').value = 2;
                break;
            case 'In Testing':
                document.getElementById('status').value = 3;
                break;
            case 'Finished':
                document.getElementById('status').value = 4;
                break;
        }
        document.getElementById('organization_name').value = params.org;
        document.getElementById('submit-button').innerHTML = 'Zaktualizuj';
    }
}