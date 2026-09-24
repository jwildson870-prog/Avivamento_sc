if ('serviceWorker' in navigator) window.addEventListener('load', () => navigator.serviceWorker.register('/static/sw.js').catch(() => {}));

// Pré-visualização da foto de perfil antes do envio.
const profilePhotoInput = document.getElementById('profile-photo-input');
const photoPreview = document.getElementById('photo-preview');
const photoPreviewImage = document.getElementById('photo-preview-image');

if (profilePhotoInput && photoPreview && photoPreviewImage) {
    profilePhotoInput.addEventListener('change', () => {
        const file = profilePhotoInput.files?.[0];
        if (!file) {
            photoPreview.hidden = true;
            photoPreviewImage.removeAttribute('src');
            return;
        }

        if (!file.type.startsWith('image/')) {
            photoPreview.hidden = true;
            photoPreviewImage.removeAttribute('src');
            return;
        }

        const objectUrl = URL.createObjectURL(file);
        photoPreviewImage.src = objectUrl;
        photoPreview.hidden = false;
    });
}



// Abre fotos de perfil em tamanho maior, preservando o formato original.
(function () {
    const lightbox = document.getElementById('image-lightbox');
    const lightboxImage = document.getElementById('image-lightbox-image');
    const closeButton = document.getElementById('image-lightbox-close');
    if (!lightbox || !lightboxImage || !closeButton) return;

    function closeLightbox() {
        lightbox.hidden = true;
        lightbox.setAttribute('aria-hidden', 'true');
        lightboxImage.removeAttribute('src');
        document.body.classList.remove('lightbox-open');
    }

    document.addEventListener('click', function (event) {
        const image = event.target.closest('.avatar img');
        if (!image) return;
        event.preventDefault();
        lightboxImage.src = image.currentSrc || image.src;
        lightboxImage.alt = image.alt || 'Foto ampliada';
        lightbox.hidden = false;
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
    });

    closeButton.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (event) {
        if (event.target.hasAttribute('data-lightbox-close')) closeLightbox();
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !lightbox.hidden) closeLightbox();
    });
}());
