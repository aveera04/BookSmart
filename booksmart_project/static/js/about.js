// ===== About Us Page – Animated Counter & Scroll Reveal =====

document.addEventListener('DOMContentLoaded', function () {

    // --- Animated number counters ---
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-target]');
        counters.forEach(function (counter) {
            const target = parseInt(counter.getAttribute('data-target'), 10);
            const duration = 1800; // ms
            const stepTime = 20;
            const totalSteps = duration / stepTime;
            let current = 0;
            const increment = target / totalSteps;

            function updateCounter() {
                current += increment;
                if (current >= target) {
                    counter.textContent = target.toLocaleString();
                    return;
                }
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(function () {
                    setTimeout(updateCounter, stepTime);
                });
            }
            updateCounter();
        });
    }

    // --- Intersection Observer for stats animation ---
    var statsSection = document.getElementById('about-stats');
    var statsAnimated = false;

    if (statsSection) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && !statsAnimated) {
                    statsAnimated = true;
                    animateCounters();
                }
            });
        }, { threshold: 0.4 });
        observer.observe(statsSection);
    }

    // --- Scroll reveal for cards ---
    var revealElements = document.querySelectorAll('.value-card, .team-card');
    if (revealElements.length > 0) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealElements.forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            revealObserver.observe(el);
        });
    }
});
