// ===== SIDEBAR NAVIGATION =====
(function() {
    const navItems = document.querySelectorAll('.sidebar-nav-item[data-section]');
    const sections = document.querySelectorAll('.profile-section');

    function showSection(sectionId) {
        sections.forEach(function(s) {
            s.style.display = 'none';
            // Reset animation
            s.style.animation = 'none';
            s.offsetHeight; // trigger reflow
            s.style.animation = '';
        });

        var target = document.getElementById('section-' + sectionId);
        if (target) {
            target.style.display = 'block';
            // Re-trigger animation
            target.style.animation = 'none';
            target.offsetHeight;
            target.style.animation = 'fadeSlideUp 0.5s ease forwards';
        }

        navItems.forEach(function(n) { n.classList.remove('active'); });
    }

    navItems.forEach(function(item) {
        item.addEventListener('click', function() {
            var section = this.getAttribute('data-section');
            showSection(section);
            this.classList.add('active');

            // On mobile, scroll to content
            if (window.innerWidth <= 968) {
                document.getElementById('profile-main').scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
})();

// ===== PASSWORD TOGGLE =====
function togglePwd(fieldId) {
    var field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
    }
}

// ===== PASSWORD STRENGTH CHECKER =====
function checkStrength(password) {
    var bars = [
        document.getElementById('str-1'),
        document.getElementById('str-2'),
        document.getElementById('str-3'),
        document.getElementById('str-4')
    ];
    var textEl = document.getElementById('strength-text');
    var score = 0;

    if (password.length >= 6) score++;
    if (password.length >= 10) score++;
    if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    var level = 0;
    if (score >= 5) level = 4;
    else if (score >= 4) level = 3;
    else if (score >= 2) level = 2;
    else if (score >= 1) level = 1;

    var classes = ['', 'weak', 'fair', 'good', 'strong'];
    var labels = ['Enter a password', 'Weak — add more characters', 'Fair — try uppercase & numbers', 'Good — almost there!', 'Strong — excellent!'];

    bars.forEach(function(bar, i) {
        bar.className = 'strength-bar';
        if (i < level) {
            bar.classList.add('active');
            bar.classList.add(classes[level]);
        }
    });

    if (textEl) textEl.textContent = labels[level];
}

function resetStrength() {
    var bars = document.querySelectorAll('.strength-bar');
    bars.forEach(function(b) { b.className = 'strength-bar'; });
    var t = document.getElementById('strength-text');
    if (t) t.textContent = 'Enter a password';
}

// ===== SHOW CORRECT SECTION ON LOAD (based on URL hash) =====
window.addEventListener('DOMContentLoaded', function() {
    var hash = window.location.hash.replace('#', '');
    if (hash) {
        var navItem = document.querySelector('.sidebar-nav-item[data-section="' + hash + '"]');
        if (navItem) navItem.click();
    }
});
