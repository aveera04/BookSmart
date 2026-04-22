// Toggle password visibility
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
    }
}

// Password strength indicator
function initPasswordStrength(inputId) {
    const pwdInput = document.getElementById(inputId);
    const bars = document.querySelectorAll('.strength-bar');

    if (pwdInput) {
        pwdInput.addEventListener('input', function () {
            const val = this.value;
            let strength = 0;
            if (val.length >= 6) strength++;
            if (val.length >= 10) strength++;
            if (/[a-z]/.test(val) && /[A-Z]/.test(val)) strength++;
            if (/\d/.test(val) && /[!@#$%^&*]/.test(val)) strength++;

            bars.forEach(function(bar, i) {
                bar.classList.remove('active', 'weak', 'medium');
                if (i < strength) {
                    if (strength === 1) bar.classList.add('weak');
                    else if (strength <= 2) bar.classList.add('medium');
                    else bar.classList.add('active');
                }
            });
        });
    }
}

// ===== TOAST SYSTEM =====
function showToast(type, title, message) {
    var icons = { success: '✅', error: '❌', info: 'ℹ️' };
    var container = document.getElementById('toast-container');
    var toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML =
        '<div class="toast-body">' +
            '<span class="toast-icon">' + (icons[type] || 'ℹ️') + '</span>' +
            '<div class="toast-text">' +
                '<div class="toast-title">' + title + '</div>' +
                '<div class="toast-msg">' + message + '</div>' +
            '</div>' +
            '<button class="toast-close" onclick="dismissToast(this.closest(\'div.toast\'))">✕</button>' +
        '</div>' +
        '<div class="toast-bar"></div>';
    container.appendChild(toast);
    requestAnimationFrame(function() {
        requestAnimationFrame(function() { toast.classList.add('show'); });
    });
    setTimeout(function() { dismissToast(toast); }, 4500);
}

function dismissToast(toast) {
    if (!toast) return;
    toast.classList.remove('show');
    setTimeout(function() { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 400);
}

// ===== RENDER DJANGO MESSAGES AS TOASTS =====
function renderDjangoMessages(msgs) {
    var titles = { success: 'Success', error: 'Error', info: 'Info', warning: 'Warning' };
    msgs.forEach(function(m) {
        var tag = m.type.split(' ')[0];
        if (tag === 'messages') tag = m.type.split(' ')[1] || 'info';
        showToast(tag, titles[tag] || 'Notice', m.text);
    });
}
