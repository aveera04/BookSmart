function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
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
    // Trigger animation
    requestAnimationFrame(function() {
        requestAnimationFrame(function() { toast.classList.add('show'); });
    });
    // Auto-dismiss after 4.5s
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
        var tag = m.type.split(' ')[0]; // handle 'messages error' compound tags
        if (tag === 'messages') tag = m.type.split(' ')[1] || 'info';
        showToast(tag, titles[tag] || 'Notice', m.text);
    });
}
