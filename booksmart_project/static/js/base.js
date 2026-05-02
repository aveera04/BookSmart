// ===== CAROUSEL FUNCTIONALITY =====
function initCarousel(trackId, prevBtnId, nextBtnId) {
    const track = document.getElementById(trackId);
    const prevBtn = document.getElementById(prevBtnId);
    const nextBtn = document.getElementById(nextBtnId);

    if (!track || !prevBtn || !nextBtn) {
        return;
    }

    let currentIndex = 0;

    function getVisibleCards() {
        const width = window.innerWidth;
        if (width <= 480) return 2;
        if (width <= 768) return 3;
        if (width <= 1024) return 4;
        return 6;
    }

    function getCardWidth() {
        const cards = track.children;
        if (cards.length === 0) return 0;
        const card = cards[0];
        const style = window.getComputedStyle(card);
        return card.offsetWidth + parseInt(style.marginRight || 0) + 18; // 18 = gap
    }

    function updateCarousel() {
        const cardWidth = getCardWidth();
        const offset = currentIndex * cardWidth;
        track.style.transform = 'translateX(-' + offset + 'px)';
    }

    function getMaxIndex() {
        const totalCards = track.children.length;
        const visible = getVisibleCards();
        return Math.max(0, totalCards - visible);
    }

    nextBtn.addEventListener('click', function() {
        const maxIndex = getMaxIndex();
        if (currentIndex < maxIndex) {
            currentIndex++;
        } else {
            currentIndex = 0; // Loop back to start
        }
        updateCarousel();
    });

    prevBtn.addEventListener('click', function() {
        const maxIndex = getMaxIndex();
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = maxIndex; // Loop to end
        }
        updateCarousel();
    });

    // Reset on resize
    window.addEventListener('resize', function() {
        const maxIndex = getMaxIndex();
        if (currentIndex > maxIndex) {
            currentIndex = maxIndex;
        }
        updateCarousel();
    });
}

// Initialize both carousels
initCarousel('featured-track', 'featured-prev', 'featured-next');
initCarousel('bestsellers-track', 'bestseller-prev', 'bestseller-next');

// ===== NAV ACTIVE STATE =====
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
        navLinks.forEach(function(l) { l.classList.remove('active'); });
        this.classList.add('active');
    });
});

// ===== NAV GENRE DROPDOWN POSITIONING =====
const genreTrigger = document.getElementById('nav-genres');
const genreMenu = document.querySelector('.dropdown-menu');

function measureMenuWidth(menu) {
    const prevDisplay = menu.style.display;
    const prevVisibility = menu.style.visibility;
    menu.style.visibility = 'hidden';
    menu.style.display = 'block';
    const width = menu.offsetWidth || 220;
    menu.style.display = prevDisplay;
    menu.style.visibility = prevVisibility;
    return width;
}

function positionGenreMenu() {
    if (!genreTrigger || !genreMenu) {
        return;
    }
    const rect = genreTrigger.getBoundingClientRect();
    const menuWidth = measureMenuWidth(genreMenu);
    const gutter = 12;
    const maxLeft = Math.max(gutter, window.innerWidth - menuWidth - gutter);
    const left = Math.min(rect.left, maxLeft);
    const top = rect.bottom + 8;
    genreMenu.style.setProperty('--dropdown-top', top + 'px');
    genreMenu.style.setProperty('--dropdown-left', left + 'px');
}

if (genreTrigger && genreMenu) {
    ['mouseenter', 'focus'].forEach(function(evt) {
        genreTrigger.addEventListener(evt, positionGenreMenu);
    });
    window.addEventListener('resize', positionGenreMenu);
}

// ===== ADD TO CART FEEDBACK =====
const cartBtns = document.querySelectorAll('.btn-add-cart');
cartBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const original = this.textContent;
        this.textContent = '✓ Added!';
        this.style.backgroundColor = '#1a7a6d';
        var self = this;
        setTimeout(function() {
            self.textContent = original;
            self.style.backgroundColor = '';
        }, 1500);
    });
});

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
// Called from inline script that passes Django template messages
function renderDjangoMessages(msgs) {
    var titles = { success: 'Success', error: 'Error', info: 'Info', warning: 'Warning' };
    msgs.forEach(function(m) {
        var tag = m.type.split(' ')[0];
        if (tag === 'messages') tag = m.type.split(' ')[1] || 'info';
        showToast(tag, titles[tag] || 'Notice', m.text);
    });
}
