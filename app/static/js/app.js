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



// Visualizador de mídia em tela cheia: fotos, vídeos e avatares.
(function () {
    const lightbox = document.getElementById('media-lightbox');
    const image = document.getElementById('media-lightbox-image');
    const video = document.getElementById('media-lightbox-video');
    const closeButton = document.getElementById('media-lightbox-close');
    if (!lightbox || !image || !video || !closeButton) return;

    function closeLightbox() {
        video.pause();
        video.removeAttribute('src');
        video.load();
        image.removeAttribute('src');
        image.hidden = true;
        video.hidden = true;
        lightbox.hidden = true;
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');
    }

    function openImage(source) {
        video.hidden = true;
        image.hidden = false;
        image.src = source.currentSrc || source.src;
        image.alt = source.alt || 'Imagem ampliada';
        lightbox.hidden = false;
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
    }

    function openVideo(source) {
        image.hidden = true;
        video.hidden = false;
        video.src = source.currentSrc || source.src;
        video.poster = source.poster || '';
        lightbox.hidden = false;
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
        video.play().catch(() => {});
    }

    document.addEventListener('click', function (event) {
        const target = event.target.closest('main img:not(.no-media-lightbox), main video:not(.no-media-lightbox)');
        if (!target || target.closest('.photo-preview')) return;
        event.preventDefault();
        if (target.tagName === 'VIDEO') openVideo(target);
        else openImage(target);
    });

    closeButton.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (event) {
        if (event.target.hasAttribute('data-lightbox-close')) closeLightbox();
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !lightbox.hidden) closeLightbox();
    });
}());
