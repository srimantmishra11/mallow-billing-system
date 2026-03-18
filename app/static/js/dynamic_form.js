// Dynamic form functionality for adding product rows

let productCount = 1;

function addProductRow() {
    const container = document.getElementById('products-container');
    productCount++;

    const row = document.createElement('div');
    row.className = 'products-row';
    row.id = `product-row-${productCount}`;
    row.innerHTML = `
        <h4>Product ${productCount}</h4>
        <div class="form-group">
            <label for="product_id_${productCount}">Product ID:</label>
            <input type="text" id="product_id_${productCount}" name="product_id_${productCount}" required>
        </div>
        <div class="form-group">
            <label for="quantity_${productCount}">Quantity:</label>
            <input type="number" id="quantity_${productCount}" name="quantity_${productCount}" min="1" required>
        </div>
        <button type="button" class="btn btn-danger" onclick="removeProductRow(${productCount})">Remove</button>
    `;

    container.appendChild(row);
}

function removeProductRow(id) {
    const row = document.getElementById(`product-row-${id}`);
    if (row) {
        row.remove();
    }
}

// API helper functions
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        let errorMessage = 'API request failed';
        try {
            const error = await response.json();
            errorMessage = error.detail || errorMessage;
        } catch (e) {
            errorMessage = response.statusText;
        }
        throw new Error(errorMessage);
    }

    return response.json();
}

// Format currency
function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}

// Show alert message
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const main = document.querySelector('main');
    main.insertBefore(alertDiv, main.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}