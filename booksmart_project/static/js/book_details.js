// ===== Book Details Page JavaScript =====

document.addEventListener('DOMContentLoaded', function () {

    // ===== TAB SWITCHING =====
    var tabBtns = document.querySelectorAll('.tab-btn');
    var tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var targetTab = this.getAttribute('data-tab');

            // Remove active from all tabs and contents
            tabBtns.forEach(function (b) { b.classList.remove('active'); });
            tabContents.forEach(function (c) { c.classList.remove('active'); });

            // Set active
            this.classList.add('active');
            var targetContent = document.getElementById('content-' + targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    // ===== WISHLIST BUTTON TOGGLE =====
    var wishlistBtn = document.getElementById('btn-wishlist');
    if (wishlistBtn) {
        var isWishlisted = false;
        wishlistBtn.addEventListener('click', function () {
            isWishlisted = !isWishlisted;
            var icon = this.querySelector('.btn-icon');
            if (isWishlisted) {
                icon.textContent = '♥';
                this.style.background = '#1e3a5f';
                this.style.color = '#ffffff';
                this.style.borderColor = '#1e3a5f';
                // Pulse animation
                this.style.transform = 'scale(1.05)';
                setTimeout(function () {
                    wishlistBtn.style.transform = '';
                }, 200);
            } else {
                icon.textContent = '♡';
                this.style.background = 'transparent';
                this.style.color = '#1e3a5f';
                this.style.borderColor = '#1e3a5f';
            }
        });
    }

    // ===== ADD TO CART BUTTON FEEDBACK =====
    var addToCartBtn = document.getElementById('btn-add-to-cart');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function () {
            var originalText = this.innerHTML;
            this.innerHTML = '<span class="btn-icon">✓</span> Added to Cart';
            this.style.background = 'linear-gradient(135deg, #1a7a6d 0%, #22a392 100%)';
            this.disabled = true;

            var btn = this;
            setTimeout(function () {
                btn.innerHTML = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 2000);
        });
    }

    // ===== STAR RATING HOVER EFFECT =====
    var stars = document.querySelectorAll('.star-rating .star');
    stars.forEach(function (star, index) {
        star.addEventListener('mouseenter', function () {
            stars.forEach(function (s, i) {
                if (i <= index) {
                    s.style.color = '#f5a623';
                    s.style.transform = 'scale(1.2)';
                } else {
                    s.style.color = '#d1d5db';
                    s.style.transform = 'scale(1)';
                }
            });
        });

        star.addEventListener('mouseleave', function () {
            stars.forEach(function (s) {
                s.style.transform = 'scale(1)';
                // Restore original state
                if (s.classList.contains('filled')) {
                    s.style.color = '#f5a623';
                } else {
                    s.style.color = '#d1d5db';
                }
            });
        });
    });

    // ===== IMAGE ZOOM ON CLICK =====
    var bookImage = document.getElementById('book-main-image');
    if (bookImage) {
        bookImage.style.cursor = 'zoom-in';
        bookImage.addEventListener('click', function () {
            // Create overlay
            var overlay = document.createElement('div');
            overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;display:flex;align-items:center;justify-content:center;cursor:zoom-out;animation:fadeIn 0.3s ease;';

            var zoomedImg = document.createElement('img');
            zoomedImg.src = bookImage.src;
            zoomedImg.alt = bookImage.alt;
            zoomedImg.style.cssText = 'max-width:90%;max-height:90%;object-fit:contain;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.5);animation:scaleIn 0.3s ease;';

            // Close button
            var closeBtn = document.createElement('button');
            closeBtn.textContent = '✕';
            closeBtn.style.cssText = 'position:absolute;top:30px;right:30px;background:rgba(255,255,255,0.15);border:none;color:#fff;font-size:24px;width:44px;height:44px;border-radius:50%;cursor:pointer;transition:background 0.3s;display:flex;align-items:center;justify-content:center;';
            closeBtn.addEventListener('mouseenter', function () { this.style.background = 'rgba(255,255,255,0.3)'; });
            closeBtn.addEventListener('mouseleave', function () { this.style.background = 'rgba(255,255,255,0.15)'; });

            overlay.appendChild(zoomedImg);
            overlay.appendChild(closeBtn);
            document.body.appendChild(overlay);
            document.body.style.overflow = 'hidden';

            function closeOverlay() {
                overlay.style.opacity = '0';
                overlay.style.transition = 'opacity 0.25s ease';
                setTimeout(function () {
                    document.body.removeChild(overlay);
                    document.body.style.overflow = '';
                }, 250);
            }

            overlay.addEventListener('click', closeOverlay);
            closeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                closeOverlay();
            });

            // ESC key to close
            var escHandler = function (e) {
                if (e.key === 'Escape') {
                    closeOverlay();
                    document.removeEventListener('keydown', escHandler);
                }
            };
            document.addEventListener('keydown', escHandler);
        });
    }
});
