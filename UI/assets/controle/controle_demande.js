
//const apiUrl = 'http://localhost:8000/Demande';  // Make sure this matches your FastAPI URL
//const apiUrlprint = 'http://localhost:8000/print'
const apiUrl = '/Demande';  // Make sure this matches your FastAPI URL
const apiUrlprint = '/print'


const modeSelect = document.getElementById('modeSelect');
const inputContainer = document.getElementById('inputContainer');
const inputLabel = document.getElementById('inputLabel');

// Listen for dropdown changes
modeSelect.addEventListener('change', function() {
    const mode = this.value;
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = String(today.getMonth() + 1).padStart(2, '0');
    const currentDay = String(today.getDate()).padStart(2, '0');

    if (mode === "full-date") {
        inputLabel.textContent = "اختر التاريخ:";
        inputContainer.innerHTML = `<input type="date" id="search_gestion" value="${currentYear}-${currentMonth}-${currentDay}">`;
    } 
    
    else if (mode === "month-year") {
        inputLabel.textContent = "اختر شهر و سنة:";
        inputContainer.innerHTML = `
  <input type="text" id="search_gestion" inputmode="numeric" placeholder="2026-07">
`;
    } 
    
});

function Change_account(){

    const Account_name = document.getElementById('Account').value;
    const Account_N = document.getElementById('search_NumCompte')
    switch (Account_name) {
        case 'BNA':
            Account_N.value = '001';
            break;
        case 'CCP':
            Account_N.value = '007';
            break;
        case 'BDL':
            Account_N.value = '005';
            break;
        case 'BADR':
            Account_N.value = '003';
            break;
        case 'TRS':
            Account_N.value = '008';
            break;
        case 'CPA':
            Account_N.value = '004';
            break;
    
        default:
            break;
    }


}


    document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("Attachments");
  const addBtn = document.getElementById("addAttachment");
  const chips = document.getElementById("attachmentsChips");
  const hidden = document.getElementById("attachmentsHidden");

  if (!input || !addBtn || !chips || !hidden) return; // page safety

  const selected = new Set();

  function syncHidden() {
    hidden.value = Array.from(selected).join(",");
  }

  function render() {
    chips.innerHTML = "";

    selected.forEach((value) => {
      const chip = document.createElement("span");
      chip.style.cssText = `
        background:#eee; border:1px solid #ddd; padding:6px 10px;
        border-radius:999px; display:inline-flex; align-items:center; gap:8px;
        font-size:14px;
      `;

      const text = document.createElement("span");
      text.textContent = value;

      const remove = document.createElement("button");
      remove.type = "button";
      remove.textContent = "×";
      remove.style.cssText = `
        cursor:pointer; border:none; background:transparent; font-size:16px; line-height:1;
      `;

      remove.addEventListener("click", () => {
        selected.delete(value);
        syncHidden();
        render();
      });

      chip.appendChild(text);
      chip.appendChild(remove);
      chips.appendChild(chip);
    });

    syncHidden();
  }

  function tryAdd() {
    const value = (input.value || "").trim();
    if (!value) return;

    if (selected.has(value)) {
      input.value = "";
      return;
    }

    selected.add(value);
    input.value = "";
    render();
  }

  addBtn.addEventListener("click", tryAdd);

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      tryAdd();
    }
  });

  render();
});  

async function searchDemandes() {
    // Get all search field values
    const demande_id = document.getElementById('search_demande_id').value;
    const numCompte = document.getElementById('search_NumCompte').value;
    const typePrestation = document.getElementById('search_type_prestation').value;
    const gestion = document.getElementById('search_gestion').value;
    const periodeDeduction = document.getElementById('search_periode_deduction').value;
    const montante = document.getElementById('search_montante').value;
    const demande_satatu = document.getElementById('search_statut').value;


     const attachments = document.getElementById('attachmentsHidden').value;
    // Build query parameters
    const params = new URLSearchParams();
    
    if (demande_id) params.append('demande_id', demande_id);
    if (numCompte) params.append('NumCompte', numCompte);
    if (typePrestation) params.append('type_prestation', typePrestation);
    if (gestion) params.append('gestion', gestion);
    if (periodeDeduction) params.append('Période_Déduction', periodeDeduction);
    if (montante) params.append('montante', montante);
    if (demande_satatu) params.append('demande_statut', demande_satatu);
    if (attachments) params.append('attachments', attachments);
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
    const tableBody = document.getElementById('demandesTableBody');
    if (!tableBody) {
        console.error("tableBody not found! Check the ID 'demandesTableBody'");
        return;
    }
    tableBody.innerHTML = '';

    let totalMontant = 0;

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
            <td>/</td>
            <td>${demande.demande_statut}</td>
            <td>
                <button onclick="deleteDemande('${demande.demande_id}')">حذف ❌</button>
            </td>
            <td>
                <button class="print-btn" onclick="printDemande(parseInt(${demande.demande_id}, 10))"> 🖨️ طباعة</button>
            </td>
        `;
        tableBody.appendChild(row);

        // Clean the montant value: remove anything that's not a digit, dot, or minus sign
        const cleanValue = String(demande.montant).replace(/[^0-9.-]+/g, '');
        const numericValue = parseFloat(cleanValue);

        if (!isNaN(numericValue)) {
            totalMontant += numericValue;
        } else {
            console.warn("Invalid montant value:", demande.montant);
        }
    });



    const totalRow = document.createElement('tr');
    totalRow.innerHTML = `
        <td colspan="7" style="text-align:right; font-weight:bold;font-size:25px;">الإجمالي:</td>
        <td style="font-weight:bold;font-size:25px;">${totalMontant.toFixed(2)}</td>
        <td colspan="3"></td>
    `;
    tableBody.appendChild(totalRow);
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