// Gestione Dello scorrimento della modale quando si clicca accedi/registrati

const container = document.getElementById('modal-container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});


loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});