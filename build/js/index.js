import 'htmx.org';

// Import only the necessary Bootstrap Modal component
import Modal from 'bootstrap/js/dist/modal';

// Initialize the Modals when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  const modalElements = document.querySelectorAll('.modal');
  modalElements.forEach((modalElement) => {
    new Modal(modalElement);
  });
});
