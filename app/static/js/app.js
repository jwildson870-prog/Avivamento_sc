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

