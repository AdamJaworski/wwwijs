function updateOrgs() {
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
            table = document.getElementById('org-table');
            data.orgs.forEach(org => {
                var tr = document.createElement('tr');
                var orgTh = document.createElement('th');
                var permTh = document.createElement('th');
                var leaveTh = document.createElement('th');
                var leaveButton = document.createElement('button');
                var ownerButton = document.createElement('button');
                orgTh.innerHTML = org.org_name;
                permTh.innerHTML = org.access_lvl;
                leaveButton.innerHTML = "Leave";
                ownerButton.innerHTML = "Get Ownership";
                ownerButton.onclick = (event) => getOwnership(org.org_name);
                leaveButton.onclick = (event) => leaveOrg(org.org_name);
                leaveButton.className = 'action-button leave-button';
                ownerButton.className = 'action-button';
                leaveTh.appendChild(leaveButton);
                leaveTh.appendChild(ownerButton);
                tr.appendChild(orgTh);
                tr.appendChild(permTh);
                tr.appendChild(leaveTh);
                table.appendChild(tr);
            });
        })
        .catch(error => console.error('Error fetching orgs:', error));
}

function leaveOrg(org_name) {
    fetch('/leave_org', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'org_name': org_name
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.status) {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } else if (data.status) {
            window.location.reload();
        }
    })
    .catch(error => console.error('Error leaving org:', error));
}

function getOwnership(org_name){
    fetch('/get_ownership', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'org_name': org_name
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.status) {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } else if (data.status) {
            window.location.reload();
        }
    })
    .catch(error => console.error('Error updating permissions:', error));
}