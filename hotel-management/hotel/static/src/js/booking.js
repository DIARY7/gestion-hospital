// Set minimum date to today
const today = new Date().toISOString().split('T')[0];
document.getElementById('checkIn').min = today;
document.getElementById('checkOut').min = today;

// Update checkout minimum date when checkin changes
document.getElementById('checkIn').addEventListener('change', function() {
    const checkInDate = new Date(this.value);
    checkInDate.setDate(checkInDate.getDate() + 1);
    document.getElementById('checkOut').min = checkInDate.toISOString().split('T')[0];
});

function updateRoomInfo() {
    const select = document.getElementById('roomNumber');
    const option = select.options[select.selectedIndex];
    const roomInfo = document.getElementById('roomInfo');

    if (option.value) {
        document.getElementById('roomType').textContent = option.dataset.type;
        document.getElementById('roomPrice').textContent = option.dataset.price;
        roomInfo.style.display = 'block';
        calculateTotal();
    } else {
        roomInfo.style.display = 'none';
        document.getElementById('priceSummary').style.display = 'none';
    }
}


function calculateTotal() {
    const roomSelect = document.getElementById('roomNumber');
    const checkIn = document.getElementById('checkIn').value;
    const checkOut = document.getElementById('checkOut').value;

    if (!roomSelect.value || !checkIn || !checkOut) {
        document.getElementById('priceSummary').style.display = 'none';
        return;
    }

    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);
    const nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));

    if (nights <= 0) {
        document.getElementById('priceSummary').style.display = 'none';
        return;
    }

    const roomPrice = parseInt(roomSelect.options[roomSelect.selectedIndex].dataset.price);
    const roomTotal = roomPrice * nights;

    // Calculate equipment costs
    const equipmentPrices = {
        breakfast: 15,
        parking: 10,
        minibar: 25,
        laundry: 20,
        spa: 30
    };

    let equipmentTotal = 0;
    let equipmentSummary = '';

    document.querySelectorAll('input[name="equipment"]:checked').forEach(checkbox => {
        const price = equipmentPrices[checkbox.value] || 0;
        const dailyTotal = checkbox.value === 'laundry' ? price : price * nights;
        equipmentTotal += dailyTotal;

        const label = checkbox.nextElementSibling.querySelector('strong').textContent;
        equipmentSummary += `<div class="d-flex justify-content-between"><span>${label}:</span><span>${dailyTotal}€</span></div>`;
    });

    const grandTotal = roomTotal + equipmentTotal;

    // Update display
    document.getElementById('nightsCount').textContent = nights;
    document.getElementById('roomTotal').textContent = roomTotal;
    document.getElementById('equipmentSummary').innerHTML = equipmentSummary;
    document.getElementById('grandTotal').textContent = grandTotal;
    document.getElementById('priceSummary').style.display = 'block';
}


