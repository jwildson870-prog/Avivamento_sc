const btnOlho = document.getElementById('btn-mostrar');
const campoSenha = document.getElementById('senha');

if (btnOlho && campoSenha) {
    btnOlho.addEventListener('click', () => {
        const mostrando = campoSenha.type === 'password';
        campoSenha.type = mostrando ? 'text' : 'password';
        btnOlho.setAttribute('aria-label', mostrando ? 'Ocultar senha' : 'Mostrar senha');
        btnOlho.setAttribute('title', mostrando ? 'Ocultar senha' : 'Mostrar senha');
        btnOlho.innerHTML = mostrando
            ? '<svg class="icone-olho" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3l18 18"></path><path d="M10.6 10.6a2 2 0 0 0 2.8 2.8"></path><path d="M9.9 5.2A10.7 10.7 0 0 1 12 5c6 0 9.5 7 9.5 7a16.7 16.7 0 0 1-3.1 3.8"></path><path d="M6.1 6.1C3.8 7.6 2.5 10 2.5 12c0 0 3.5 7 9.5 7 1.1 0 2.1-.2 3-.6"></path></svg>'
            : '<svg class="icone-olho" viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z"></path><circle cx="12" cy="12" r="2.5"></circle></svg>';
    });
}
