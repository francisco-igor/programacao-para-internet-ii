document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", openDeleteModal);
    });

    document.querySelectorAll(".btn-secondary").forEach(button => {
        button.addEventListener("click", closeDeleteModal);
    });
});

// Função para abrir o modal
function openDeleteModal() {
    const modalId = this.getAttribute("data-id");
    document.getElementById(`modal-delete-${modalId}`).style.display = "block";
}

// Função para fechar o modal
function closeDeleteModal() {
    const modalId = this.getAttribute("data-id");
    document.getElementById(`modal-delete-${modalId}`).style.display = "none";
}
