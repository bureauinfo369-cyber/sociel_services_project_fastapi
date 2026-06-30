
//const apiUrl = 'http://localhost:8000/Emploiyes'; 
const apiUrl = '/Emploiyes'; 
console.log(window.location.origin);
// Search employees function
async function searchEmployees() {
    // Get all search field values
    const numCompte = document.getElementById('NumCompte').value;
    const nom = document.getElementById('Nom').value;
    const grade = document.getElementById('Grade').value;
    const poste = document.getElementById('Poste').value;
    const lieuDeTravail = document.getElementById('lieu_de_travail').value;
    const residence_admin = document.getElementById('residence_admin').value;
    // Build query parameters
    const params = new URLSearchParams();
    
    if (numCompte) params.append('NumCompte', numCompte);
    if (nom) params.append('Nom', nom);
    if (grade) params.append('Grade', grade);
    if (poste) params.append('Poste', poste);
    if (lieuDeTravail) params.append('lieu_de_travail', lieuDeTravail);
    if (residence_admin) params.append('residence_admin', residence_admin);
    
    // Check if at least one field is filled
    if (params.toString() === '') {
        alert('Veuillez entrer au moins un critère de recherche');
        return;
    }
    
    try {
        const response = await fetch(`${apiUrl}/search/?${params.toString()}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const employees = await response.json();
        console.log('Search results:', employees);
        
        displayEmployees(employees);
        
    } catch (error) {
        console.error('Error searching employees:', error);
        alert('Erreur: ' + error.message);
    }
}

// Clear search function
function clearSearch() {
    document.getElementById('NumCompte').value = '';
    document.getElementById('Nom').value = '';
    document.getElementById('Grade').value = '';
    document.getElementById('Poste').value = '';
    document.getElementById('lieu_de_travail').value = '';
    document.getElementById('residence_admin').value = '';
    
    fetchAllEmployees(); // Show all employees again
}

// Function to fetch and display all employees
async function fetchAllEmployees() {
    try {
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const employees = await response.json();
        console.log('Fetched all employees:', employees);
        
        // Handle both array and single object responses
        const employeesArray = Array.isArray(employees) ? employees : [employees];
        displayEmployees(employeesArray);
        
    } catch (error) {
        console.error('Error fetching all employees:', error);
        alert('Erreur de chargement des employés: ' + error.message);
    }
}

// Function to display employees in the table
function displayEmployees(employees) {
    const tableBody = document.getElementById('EmploiyesTableBody');
    tableBody.innerHTML = ''; // Clear existing rows
    
    employees.forEach(employee => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td style="padding-left:10px;">${employee.NumCompte}</td>
            <td>${employee.Nom}</td>
            <td>${employee.Grade}</td>
            <td>${employee.Poste}</td>
            <td>${employee.lieu_de_travail}</td>
            <td>${employee.residence_admin}</td>
            <td>
                
                <button onclick="editEmployee('${employee.NumCompte}')" class="delete-btn" style="color: green;">تعديل ✏️</button>
            </td>
            <td>
            <button onclick="deleteEmployee('${employee.NumCompte}')" class="delete-btn" style="color: red;">حذف ❌</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Function to add a new employee
async function addEmployee() {
    const numCompte = document.getElementById('NumCompte').value;
    const nom = document.getElementById('Nom').value;
    const grade = document.getElementById('Grade').value;
    const poste = document.getElementById('Poste').value;
    const lieuDeTravail = document.getElementById('lieu_de_travail').value;
    const residence_admin = document.getElementById('residence_admin').value;
    
    // Validate required fields
    if (!numCompte || !nom || !grade || !poste || !lieuDeTravail || !residence_admin) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
    }
    
    // Validate field lengths (adjust these based on your database column sizes)
    if (numCompte.length != 20 ) {
        alert('Numéro de Compte trop long ou courte (20 caractères)');
        return;
    }
    if (nom.length > 50) {
        alert('Nom trop long (max 50 caractères)');
        return;
    }
    if (grade.length > 30) {
        alert('Grade trop long (max 30 caractères)');
        return;
    }
    if (poste.length > 50) {
        alert('Poste trop long (max 50 caractères)');
        return;
    }
    if (lieuDeTravail.length > 30) {
        alert('Lieu de travail trop long (max 30 caractères)');
        return;
    }
    if (residence_admin.length > 20) {
        alert('Lieu de travail trop long (max 20 caractères)');
        return;
    }
    
    const newEmployee = {
        NumCompte: numCompte,
        Nom: nom,
        Grade: grade,
        Poste: poste,
        lieu_de_travail: lieuDeTravail,
        residence_admin:residence_admin
    };

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newEmployee),
        });
        
        if (response.ok) {
            alert('Employé ajouté avec succès!');
            clearAddForm();
            fetchAllEmployees();
        } else {
            const errorData = await response.json();
            console.error('Full error response:', errorData);
            alert('Erreur: ' + JSON.stringify(errorData, null, 2));
        }
    } catch (error) {
        console.error('Error adding employee:', error);
        alert('Erreur lors de l\'ajout: ' + error.message);
    }
}

// Function to clear add form
function clearAddForm() {
    document.getElementById('NumCompte').value = '';
    document.getElementById('Nom').value = '';
    document.getElementById('Grade').value = '';
    document.getElementById('Poste').value = '';
    document.getElementById('lieu_de_travail').value = '';
    document.getElementById('residence_admin').value = '';
}

// Function to delete an employee
async function deleteEmployee(numCompte) {
    // Confirm before deleting
    if (!confirm(`Êtes-vous sûr de vouloir supprimer l'employé ${numCompte}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${apiUrl}/${numCompte}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            alert('Employé supprimé avec succès!');
            fetchAllEmployees(); // Refresh the table
        } else {
            const errorData = await response.json();
            console.error('Error deleting employee:', errorData);
            alert('Erreur: ' + JSON.stringify(errorData, null, 2));
        }
    } catch (error) {
        console.error('Error deleting employee:', error);
        alert('Erreur lors de la suppression: ' + error.message);
    }
}

// Function to edit an employee (placeholder - implement based on your needs)
function editEmployee(numCompte) {
    // You can implement this to show a modal or form to edit the employee
    alert(`Fonction de modification pour l'employé ${numCompte} - À implémenter`);

    
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', searchEmployees);
    }
    
    // Add functionality
    const addBtn = document.getElementById('addBtn');
    if (addBtn) {
        addBtn.addEventListener('click', addEmployee);
    }
    
    // Clear search functionality
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearSearch);
    }
    
    // Load all employees on page load
    fetchAllEmployees();
});