document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('header');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            const open = navMenu.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', String(open));
        });

        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('open')) {
                navMenu.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
                navToggle.focus();
            }
        });
    }

    if (header) {
        let scrolled = false;
        const onScroll = () => {
            const next = window.scrollY > 8;
            if (next !== scrolled) {
                scrolled = next;
                header.classList.toggle('scrolled', next);
            }
        };
        onScroll();
        window.addEventListener('scroll', onScroll, { passive: true });
    }

    const slides = document.querySelectorAll('.slide');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (slides.length > 1 && !reduceMotion) {
        let idx = 0;
        let timer = null;
        const tick = () => {
            slides[idx].classList.remove('active');
            idx = (idx + 1) % slides.length;
            slides[idx].classList.add('active');
        };
        const start = () => { if (!timer) timer = setInterval(tick, 5000); };
        const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
        start();
        document.addEventListener('visibilitychange', () => {
            document.hidden ? stop() : start();
        });
    }
});
