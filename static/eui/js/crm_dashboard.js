/**
 * CRM Dashboard JavaScript with JWT Authentication
 */

// Global state
let currentOrganizationId = null;

// Execute API requests with JWT authentication
// Execute API requests with JWT authentication or fallback to session auth
async function fetchApi(url) {
    try {
        // Get token from localStorage
        const token = localStorage.getItem('access_token');
        
        const headers = {
            'Accept': 'application/json'
        };
        
        // Add token if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: headers,
            // Include credentials for session-based auth as fallback
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            // Check if token is expired
            if (response.status === 401) {
                console.warn('Authentication issue. Might need to log in again.');
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error fetching from ${url}:`, error);
        throw error;
    }
}

// Fetch organizations from the API
async function fetchOrganizations() {
    // print log to console
    console.log('Fetching organizations...');
    try {
        const data = await fetchApi('/crm/api/organizations/');
        
        console.log('Organizations fetched:', data, data.data);
        if (data.data && data.data.length > 0) {
            displayOrganizations(data.data);
            
            // Auto-select first organization if available
            if (data.data.length > 0) {
                selectOrganization(data.data[0].id, data.data[0].name);
            }
        } else {
            displayNoOrganizations();
        }
    } catch (error) {
        displayNoOrganizations();
    }
}

// Display organizations in the UI - now showing just top 5
function displayOrganizations(organizations) {
    console.log("Displaying organizations:", organizations);
    
    const container = document.getElementById('organizations-list');
    console.log("Container element:", container);
    
    if (!container) {
        console.error("Could not find organizations-list element!");
        return;
    }
    
    // Check if we have valid data
    if (!Array.isArray(organizations) || organizations.length === 0) {
        console.warn("No organizations data to display");
        displayNoOrganizations();
        return;
    }
    
    // Clear the container
    container.innerHTML = '';
    
    // Update header if it exists
    const header = document.getElementById('organizations-header');
    if (header) {
        header.textContent = "Your Top 5 Organizations";
    }
    
    // Loop through and create organization cards
    organizations.forEach(org => {
        console.log("Processing organization:", org);
        
        // Check if org has the expected properties
        if (!org.id || !org.name) {
            console.warn("Organization missing required properties:", org);
            return; // Skip this org
        }
        
        const col = document.createElement('div');
        col.className = 'col-md-4 col-lg-3';
        
        const logoUrl = org.logo ? org.logo : '';
        const tintColor = org.tint_color ? org.tint_color : '#4361ee';
        
        col.innerHTML = `
            <div class="card organization-card" data-id="${org.id}" onclick="selectOrganization(${org.id}, '${org.name}')">
                <div class="card-body d-flex flex-column align-items-center text-center p-4">
                    <div class="organization-logo mb-3" style="background-color: ${tintColor}20; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; overflow: hidden; border-radius: 8px;">
                        ${logoUrl ? 
                          `<img src="${logoUrl}" alt="${org.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;">` : 
                          `<span class="organization-placeholder">${org.name.charAt(0)}</span>`}
                    </div>
                    <h5 class="card-title" style="color: ${tintColor};">${org.name}</h5>
                    <p class="card-text text-muted small">${org.organization_type === 1 ? 'Organization' : 'Person'}</p>
                </div>
            </div>
        `;
        
        container.appendChild(col);
    });
    
    console.log("Finished displaying organizations");
}
// Display a message when no organizations are found
function displayNoOrganizations() {
    const container = document.getElementById('organizations-list');
    container.innerHTML = `
        <div class="col-12">
            <div class="empty-state">
                <i class="bi bi-building"></i>
                <h5>No organizations found</h5>
                <p>You don't have any organizations yet.</p>
            </div>
        </div>
    `;
}

// Handle organization selection
function selectOrganization(orgId, orgName) {
    if (orgId === currentOrganizationId) {
        console.log('Organization already selected:', orgId, orgName);
        return; // No need to re-fetch if already selected
    }
    // Highlight the selected organization card
    console.log('Selected organization:', orgId, orgName);
    document.querySelectorAll('.organization-card').forEach(card => {
        card.classList.remove('border-primary');
    });
    
    document.querySelector(`.organization-card[data-id="${orgId}"]`).classList.add('border-primary');
    
    // Set the current organization ID
    currentOrganizationId = orgId;
    
    // Update UI elements
    document.getElementById('btn-add-client').disabled = false;
    document.getElementById('btn-add-employee').disabled = false;
    document.getElementById('client-search').disabled = false;
    document.getElementById('employee-search').disabled = false;
    
    // Fetch clients and employees for the selected organization
    fetchClients(orgId);
    fetchEmployees(orgId);
}

// Fetch clients for the selected organization
async function fetchClients(orgId) {
    document.getElementById('clients-list').innerHTML = `
        <tr>
            <td colspan="7" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </td>
        </tr>
    `;
    
    try {
        const data = await fetchApi(`/crm/api/clients/?organization_id=${orgId}`);
        
        if (data.data && data.data.length > 0) {
            displayClients(data.data);
        } else {
            displayNoClients();
        }
    } catch (error) {
        displayNoClients();
    }
}

// Display clients in the UI
function displayClients(clients) {
    const container = document.getElementById('clients-list');
    container.innerHTML = '';
    
    clients.forEach((client, index) => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${client.user.first_name} ${client.user.last_name}</td>
            <td>${client.user.email || '-'}</td>
            <td>${client.phone_number || '-'}</td>
            <td>${client.account ? client.account.balance : '0.00'}</td>
            <td>${client.account ? client.account.cashback : '0.00'}</td>
            <td>
                <a href="/crm/clients/${client.id}/" class="btn btn-sm btn-outline-primary me-1">
                    <i class="bi bi-eye"></i>
                </a>
                <button class="btn btn-sm btn-outline-success me-1" onclick="editClient(${client.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteClient(${client.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        
        container.appendChild(row);
    });
}

// Display a message when no clients are found
function displayNoClients() {
    const container = document.getElementById('clients-list');
    container.innerHTML = `
        <tr>
            <td colspan="7">
                <div class="empty-state">
                    <i class="bi bi-people"></i>
                    <h5>No clients found</h5>
                    <p>This organization doesn't have any clients yet.</p>
                </div>
            </td>
        </tr>
    `;
}

// Fetch employees for the selected organization
async function fetchEmployees(orgId) {
    document.getElementById('employees-list').innerHTML = `
        <tr>
            <td colspan="6" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </td>
        </tr>
    `;
    
    try {
        const data = await fetchApi(`/crm/api/employees/?organization_id=${orgId}`);
        
        if (data.data && data.data.length > 0) {
            displayEmployees(data.data);
        } else {
            displayNoEmployees();
        }
    } catch (error) {
        displayNoEmployees();
    }
}

// Display employees in the UI
function displayEmployees(employees) {
    const container = document.getElementById('employees-list');
    container.innerHTML = '';
    
    employees.forEach((employee, index) => {
        const row = document.createElement('tr');
        
        const roles = employee.roles_list.map(role => role.title).join(', ');
        const status = employee.is_working_now ? 
            '<span class="badge bg-success">Active</span>' : 
            '<span class="badge bg-secondary">Inactive</span>';
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${employee.user_details.first_name} ${employee.user_details.last_name}</td>
            <td>${employee.user_details.email || '-'}</td>
            <td>${roles || '-'}</td>
            <td>${status}</td>
            <td>
                <a href="/crm/employees/${employee.id}/" class="btn btn-sm btn-outline-primary me-1">
                    <i class="bi bi-eye"></i>
                </a>
                <button class="btn btn-sm btn-outline-success me-1" onclick="editEmployee(${employee.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteEmployee(${employee.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        
        container.appendChild(row);
    });
}

// Display a message when no employees are found
function displayNoEmployees() {
    const container = document.getElementById('employees-list');
    container.innerHTML = `
        <tr>
            <td colspan="6">
                <div class="empty-state">
                    <i class="bi bi-person-badge"></i>
                    <h5>No employees found</h5>
                    <p>This organization doesn't have any employees yet.</p>
                </div>
            </td>
        </tr>
    `;
}

// Client action handlers
function editClient(clientId) {
    // Placeholder for edit client functionality
    alert(`Edit client with ID ${clientId}`);
}

function deleteClient(clientId) {
    // Placeholder for delete client functionality
    if (confirm(`Are you sure you want to delete client with ID ${clientId}?`)) {
        alert('Client deletion would happen here');
    }
}

// Employee action handlers
function editEmployee(employeeId) {
    // Placeholder for edit employee functionality
    alert(`Edit employee with ID ${employeeId}`);
}

function deleteEmployee(employeeId) {
    // Placeholder for delete employee functionality
    if (confirm(`Are you sure you want to delete employee with ID ${employeeId}?`)) {
        alert('Employee deletion would happen here');
    }
}

// Handle filter logic for search inputs
function setupSearchHandlers() {
    // Handle client search
    document.getElementById('client-search').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#clients-list tr');
        
        rows.forEach(row => {
            if (row.querySelector('td.empty-state-cell')) return;
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
    
    // Handle employee search
    document.getElementById('employee-search').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#employees-list tr');
        
        rows.forEach(row => {
            if (row.querySelector('td.empty-state-cell')) return;
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// Button action handlers
function setupButtonHandlers() {
    // Add client button click handler
    document.getElementById('btn-add-client').addEventListener('click', function() {
        if (!currentOrganizationId) {
            alert('Please select an organization first');
            return;
        }
        
        // Redirect to client creation page or show a modal
        window.location.href = `/crm/clients/add/?organization_id=${currentOrganizationId}`;
    });
    
    // Add employee button click handler
    document.getElementById('btn-add-employee').addEventListener('click', function() {
        if (!currentOrganizationId) {
            alert('Please select an organization first');
            return;
        }
        
        // Redirect to employee creation page or show a modal
        window.location.href = `/crm/employees/add/?organization_id=${currentOrganizationId}`;
    });
}

// Initialize the dashboard
function initDashboard() {
    // Fetch organizations when the page loads
    console.log('Initializing dashboard...');
    fetchOrganizations();
    
    // Set up event handlers
    setupSearchHandlers();
    setupButtonHandlers();
}

// Run initialization when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initDashboard);