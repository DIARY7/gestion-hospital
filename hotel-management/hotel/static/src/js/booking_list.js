function toggleDetails(detailsId) {
    const details = document.getElementById(detailsId);
    const button = event.target;

    if (details.classList.contains('show')) {
        details.classList.remove('show');
        button.innerHTML = '📋 Voir détails';
    } else {
        // Hide all other details first
        document.querySelectorAll('.details-section').forEach(section => {
            section.classList.remove('show');
        });
        document.querySelectorAll('.reservation-actions button').forEach(btn => {
            if (btn.innerHTML.includes('Masquer')) {
                btn.innerHTML = '📋 Voir détails';
            }
        });

        details.classList.add('show');
        button.innerHTML = '📋 Masquer détails';
    }
}

function filterReservations(status) {
    const cards = document.querySelectorAll('.reservation-card');
    const emptyState = document.getElementById('emptyState');
    let visibleCount = 0;

    cards.forEach(card => {
        if (status === 'all' || card.dataset.status === status) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    // Update count
    document.getElementById('reservationCount').textContent = visibleCount;

    // Show/hide empty state
    if (visibleCount === 0) {
        emptyState.style.display = 'block';
        document.getElementById('reservationsList').style.display = 'none';
    } else {
        emptyState.style.display = 'none';
        document.getElementById('reservationsList').style.display = 'block';
    }
}

function cancelReservation(reservationId) {
    if (confirm('Êtes-vous sûr de vouloir annuler cette réservation ?')) {
        // Here you would normally send a request to your server
        alert(`Réservation ${reservationId} annulée avec succès. Vous recevrez un email de confirmation.`);
        // For demo purposes, you could update the UI here
        // location.reload();
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set initial count
    const totalReservations = document.querySelectorAll('.reservation-card').length;
    document.getElementById('reservationCount').textContent = totalReservations;
});