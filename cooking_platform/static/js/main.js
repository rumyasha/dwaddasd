// Обработка добавления в избранное
document.addEventListener('DOMContentLoaded', function() {
    // Функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Обработка добавления/удаления из избранного
    document.querySelectorAll('.toggle-favorite').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const slug = this.dataset.recipeSlug;
            fetch(`/recipes/${slug}/favorite/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const icon = this.querySelector('i');
                    if (data.action === 'added') {
                        icon.classList.remove('bi-heart');
                        icon.classList.add('bi-heart-fill');
                        this.classList.remove('btn-outline-danger');
                        this.classList.add('btn-danger');
                    } else {
                        icon.classList.remove('bi-heart-fill');
                        icon.classList.add('bi-heart');
                        this.classList.remove('btn-danger');
                        this.classList.add('btn-outline-danger');
                    }

                    // Обновление счетчика в навигации, если есть
                    const favoritesCount = document.getElementById('favorites-count');
                    if (favoritesCount) {
                        fetch('/recipes/favorites/count/')
                            .then(response => response.json())
                            .then(data => {
                                favoritesCount.textContent = data.count;
                            });
                    }
                }
            });
        });
    });

    // Обработка добавления/удаления из сохраненных
    document.querySelectorAll('.toggle-save').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const slug = this.dataset.recipeSlug;
            fetch(`/recipes/${slug}/save/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const icon = this.querySelector('i');
                    if (data.action === 'added') {
                        icon.classList.remove('bi-bookmark');
                        icon.classList.add('bi-bookmark-fill');
                        this.classList.remove('btn-outline-primary');
                        this.classList.add('btn-primary');
                    } else {
                        icon.classList.remove('bi-bookmark-fill');
                        icon.classList.add('bi-bookmark');
                        this.classList.remove('btn-primary');
                        this.classList.add('btn-outline-primary');
                    }
                }
            });
        });
    });

    // Инициализация tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Инициализация popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Функция для отображения уведомлений
function showAlert(message, type='success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('main.container');
    if (container) {
        container.prepend(alertDiv);

        // Автоматическое закрытие через 5 секунд
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            alert.close();
        }, 5000);
    }
}