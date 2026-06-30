
//const apiUrl = 'http://localhost:8000/Demande';  // Make sure this matches your FastAPI URL
//const apiUrlprint = 'http://localhost:8000/print'
const apiUrl = '/Demande';  // Make sure this matches your FastAPI URL
const apiUrlprint = '/print'
async function searchDemandes() {
    // Get all search field values
    const demande_id = document.getElementById('search_demande_id').value;
    const numCompte = document.getElementById('search_NumCompte').value;
    const typePrestation = document.getElementById('search_type_prestation').value;
    const gestion = document.getElementById('search_gestion').value;
    const periodeDeduction = document.getElementById('search_periode_deduction').value;
    const montante = document.getElementById('search_montante').value;
    const demande_satatu = document.getElementById('search_statut').value;

    
    
    // Build query parameters
    const params = new URLSearchParams();
    
    if (demande_id) params.append('demande_id', demande_id);
    if (numCompte) params.append('NumCompte', numCompte);
    if (typePrestation) params.append('type_prestation', typePrestation);
    if (gestion) params.append('gestion', gestion);
    if (periodeDeduction) params.append('Période_Déduction', periodeDeduction);
    if (montante) params.append('montante', montante);
    if (demande_satatu) params.append('demande_satatu', demande_satatu);
    // Check if at least one field is filled
    if (params.toString() === '') {
        alert('Please enter at least one search criteria');
        return;
    }
    
    try {
        const response = await fetch(`${apiUrl}/search/?${params.toString()}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const demandes = await response.json();
        console.log('Search results:', demandes);
        
        displayDemandes(demandes);
        
    } catch (error) {
        console.error('Error searching demandes:', error);
        alert('Error: ' + error.message);
    }
}

// Clear search function
function clearSearch() {
    document.getElementById('search_demande_id').value = '';
    document.getElementById('search_NumCompte').value = '';
    document.getElementById('search_type_prestation').value = '';
    document.getElementById('search_gestion').value = '';
    document.getElementById('search_periode_deduction').value = '';
    document.getElementById('search_montante').value = '';
    document.getElementById('search_statut').value = '';
    
    fetchAllDemandes(); // Show all demandes again
}
// Function to fetch and display all demandes
async function fetchAllDemandes() {
    try {
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const demandes = await response.json();
        console.log('Fetched all demandes:', demandes);
        
        // Handle both array and single object responses
        const demandesArray = Array.isArray(demandes) ? demandes : [demandes];
        displayDemandes(demandesArray);
        
    } catch (error) {
        console.error('Error fetching all demandes:', error);
        alert('Error loading demandes: ' + error.message);
    }
}



// Function to display demandes in the table
function displayDemandes(demandes) {
    const tableBody = document.getElementById('demandesTableBody'); // Make sure your table has this ID
    tableBody.innerHTML = ''; // Clear existing rows
    demandes.forEach(demande => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td style="padding-left:10px;">${demande.demande_id}</td>
            <td>${demande.employee_name}</td>
            <td>${demande.NumCompte}</td>
            <td>${demande.type_prestation}</td>
            <td>${demande.gestion}</td>
            <td>${demande.Période_Déduction}</td>
            <td>${demande.Début_Déduction}</td>
            <td>${demande.montant}</td>
            <td>${demande.demande_statut}</td>
            
            <td>
                <button onclick="deleteDemande('${demande.demande_id}')">حذف ❌</button>
                
            </td>
            <td>
                <button class="print-btn" onclick="printDemande(parseInt(${demande.demande_id}, 10))"> 🖨️ طباعة</button>
                
            </td>
        `;
        tableBody.appendChild(row);
    });
}




//#there is a probleme in this part of code


function addMonths(startDate, monthsToAdd) {
    // Create a new date object to avoid modifying the original date
    let newDate = new Date(startDate);
    
    // Set the new month correctly by using setMonth
    newDate.setMonth(newDate.getMonth() + monthsToAdd);
    
    // Get the resulting month and year
    const newMonth = newDate.getMonth() + 1; // Months are zero-indexed
    const newYear = newDate.getFullYear();
    
    return `${newMonth.toString().padStart(2, '0')}/${newYear}`;
}

function getStartAndFinishDates(startDate, monthsToAdd) {
    const start = addMonths(startDate, 0); // Start date (no months added)
    const finish = addMonths(startDate, monthsToAdd); // Finish date (months added)

    return {
        start,
        finish
    };
}


//#




// Function to add a new demande
async function addDemande() {
    const newNumCompte = document.getElementById('search_NumCompte').value;
    const newTypePrestation = document.getElementById('search_type_prestation').value;
    const gestion = document.getElementById('search_gestion').value;
    const Période_Déduction = document.getElementById('search_periode_deduction').value;
    const montante = parseFloat(document.getElementById('search_montante').value);
    const demande_statut = document.getElementById('search_statut').value;   
    const currentDate = new Date(); // Current date
    const isLoanType = ['قرض مالي', 'قرض تقسيط'].includes(newTypePrestation);

const newDemande = {
    NumCompte: newNumCompte,
    type_prestation: newTypePrestation,
    gestion: gestion,
    montant: montante,
    demande_statut: demande_statut,
};

if (isLoanType) {
    const monthsToAdd = Période_Déduction;
    const dates = getStartAndFinishDates(currentDate, monthsToAdd);
    
    newDemande.Période_Déduction = Période_Déduction;
    newDemande.Début_Déduction = dates.start;
    newDemande.Fin_Déduction = dates.finish;
} else {
    newDemande.Période_Déduction = '';
    newDemande.Début_Déduction = '';
    newDemande.Fin_Déduction = '';
}
    

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newDemande),
        });
        if (response.ok) {
            fetchAllDemandes();
        } else {
            // THIS IS THE IMPORTANT PART - Get the actual error details
            const errorData = await response.json();
            console.error('Full error response:', errorData);
            alert('Error: ' + JSON.stringify(errorData, null, 2));
        }
    } catch (error) {
        console.error('Error adding demande:', error);
    }
}

// Function to delete a demande
// Delete a demande
async function deleteDemande(demande_id) {
    // Confirm before deleting
    if (!confirm(`Are you sure you want to delete demande #${demande_id}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${apiUrl}/${demande_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            alert('Demande deleted successfully!');
            fetchAllDemandes(); // Refresh the table
        } else {
            const errorData = await response.json();
            console.error('Error deleting demande:', errorData);
            alert('Error: ' + JSON.stringify(errorData, null, 2));
        }
    } catch (error) {
        console.error('Error deleting demande:', error);
        alert('Error deleting demande: ' + error.message);
    }
}

// UI Helper functions
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type}`;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }


async function printDemande(demandeId) {
    try {
        showLoading();
        const response = await fetch(`${apiUrlprint}/${demandeId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        hideLoading();

        // Optional: log or use the returned info
        console.log('PDF generated at:', data.pdf_path);
        console.log('Document type:', data.document_type);

        showNotification('تم إنشاء ملف PDF بنجاح!', 'success');

    } catch (error) {
        console.error('Failed to print demande:', error);
        hideLoading();

        // Show more specific error if available
        const message = error.message.includes('Unknown type_prestation')
            ? 'نوع الوثيقة غير معروف'
            : 'خطأ في إنشاء ملف PDF';

        showNotification(message, 'error');
    }
}
// Event Listeners
document.getElementById('searchBtn').addEventListener('click', searchDemandes);
document.getElementById('addBtn').addEventListener('click', addDemande);

// Call this when the page loads
window.addEventListener('DOMContentLoaded', fetchAllDemandes);