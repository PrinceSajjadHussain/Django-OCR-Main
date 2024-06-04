document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loading = document.getElementById('loading');
    const result = document.querySelector('.result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        loading.style.display = 'block';
        result.style.display = 'none';

        const formData = new FormData(form);

        fetch('', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            loading.style.display = 'none';
            result.innerHTML = data;
            result.style.display = 'block';
            result.classList.add('fade-in');
        })
        .catch(error => {
            console.error('Error:', error);
            loading.style.display = 'none';
        });
    });
});
