document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('role');
    const teacherFields = document.getElementById('teacher-fields');

    if (roleSelect && teacherFields) {
        roleSelect.addEventListener('change', function() {
            if (this.value === 'teacher') {
                teacherFields.style.display = 'block';
                const inputs = teacherFields.querySelectorAll('input');
                inputs.forEach(input => input.setAttribute('required', 'true'));
            } else {
                teacherFields.style.display = 'none';
                const inputs = teacherFields.querySelectorAll('input');
                inputs.forEach(input => {
                    input.removeAttribute('required');
                    input.value = '';
                });
            }
        });
    }

    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    const confirmButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('.teacher-row, .request-item');

            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    const toggleButtons = document.querySelectorAll('[data-toggle]');
    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('data-toggle'));
            if (target) {
                target.classList.toggle('hidden');
            }
        });
    });

    const autoHideAlerts = document.querySelectorAll('.alert:not(.alert-info)');
    autoHideAlerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

function toggleTeacherFields() {
    const roleSelect = document.getElementById('role');
    const teacherFields = document.getElementById('teacher-fields');

    if (roleSelect && teacherFields) {
        if (roleSelect.value === 'teacher') {
            teacherFields.style.display = 'block';
            const inputs = teacherFields.querySelectorAll('input');
            inputs.forEach(input => input.setAttribute('required', 'true'));
        } else {
            teacherFields.style.display = 'none';
            const inputs = teacherFields.querySelectorAll('input');
            inputs.forEach(input => {
                input.removeAttribute('required');
                input.value = '';
            });
        }
    }
}

function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

function showToast(message, type) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'info');
    
    const icons = { success: 'check_circle', error: 'cancel', warning: 'warning', info: 'info' };
    const icon = icons[type] || 'info';
    
    toast.innerHTML = '<div class="toast-content"><span class="material-symbols-outlined toast-icon">' + icon + '</span><span class="toast-message">' + message + '</span></div><button class="toast-close" onclick="this.parentElement.remove()"><span class="material-symbols-outlined">close</span></button>';
    
    container.appendChild(toast);
    
    setTimeout(function() {
        toast.classList.add('toast-hiding');
        setTimeout(function() {
            if (toast.parentElement) toast.remove();
        }, 300);
    }, 4000);
}