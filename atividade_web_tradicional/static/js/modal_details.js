document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".btn-details").forEach(button => {
        button.addEventListener("click", openDetailsModal);
    });

    document.querySelectorAll(".btn-secondary").forEach(button => {
        button.addEventListener("click", closeDetailsModal);
    });
});

// Função para abrir o modal
function openDetailsModal() {
    const modalId = this.getAttribute("data-id");
    document.getElementById(`modal-details-${modalId}`).style.display = "block";
}

// Função para fechar o modal
function closeDetailsModal() {
    const modalId = this.getAttribute("data-id");
    document.getElementById(`modal-details-${modalId}`).style.display = "none";
}
