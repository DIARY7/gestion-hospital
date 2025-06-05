function calculateTotal() {

    const nights = Number(document.getElementById("nightsCount").textContent);
    const roomTotal = Number(document.getElementById("roomTotal").textContent);

    let equipmentTotal = 0
    let equipmentSummary = ''
    document.querySelectorAll('input[name="equipment"]:checked').forEach(checkbox => {
        const price = Number(checkbox.dataset.price) || 0;
        const dailyTotal = checkbox.value === 'laundry' ? price : price * nights;
        equipmentTotal += Number(dailyTotal);

        const label = checkbox.nextElementSibling.querySelector('strong').textContent;
        equipmentSummary += `<div class="d-flex justify-content-between"><span>${label}:</span><span>${dailyTotal}Ar</span></div>`;
    });

    const grandTotal = Number(roomTotal) + Number(equipmentTotal);

    // Update display
    document.getElementById('nightsCount').textContent = nights;
    document.getElementById('roomTotal').textContent = roomTotal;
    document.getElementById('equipmentSummary').innerHTML = equipmentSummary;
    document.getElementById('grandTotal').textContent = grandTotal;
    document.getElementById('priceSummary').style.display = 'block';
}

calculateTotal()
document.querySelectorAll('.equipment-item').forEach(item => {
        item.addEventListener('click', function(e) {
            calculateTotal()
        });
    });

function toggleEquipment(element, equipmentId) {
    console.log("cliquer")
    const checkbox = document.getElementById(equipmentId);
    checkbox.checked = !checkbox.checked;

    if (checkbox.checked) {
        element.classList.add('selected');
    } else {
        element.classList.remove('selected');
    }

    calculateTotal();
}
