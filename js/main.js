/* ============================================
   P.Ricaldone — Portfolio
   Shared JavaScript
   ============================================ */

(function() {
    'use strict';

    /* ----------------------------------------
       Theme Management (with localStorage)
       ---------------------------------------- */
    const html = document.documentElement;
    const THEME_KEY = 'pricaldone-theme';

    // Theme is already applied by inline script in <head> to prevent FOUC.
    // If not set yet, default to dark.
    if (!html.getAttribute('data-theme')) {
        html.setAttribute('data-theme', 'dark');
    }

    function initThemeToggle() {
        const toggle = document.querySelector('.theme-toggle');
        if (!toggle) return;

        toggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem(THEME_KEY, next);
        });
    }

    /* ----------------------------------------
       Custom Cursor (pointer: fine only)
       ---------------------------------------- */
    function initCursor() {
        if (!window.matchMedia('(pointer: fine)').matches) return;

        const cursor = document.querySelector('.cursor-dot');
        if (!cursor) return;

        let mouseX = 0, mouseY = 0;
        let cursorX = 0, cursorY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        document.addEventListener('mousedown', () => cursor.classList.add('click'));
        document.addEventListener('mouseup', () => cursor.classList.remove('click'));

        document.addEventListener('mouseout', (e) => {
            if (!e.relatedTarget) cursor.style.opacity = '0';
        });
        document.addEventListener('mouseover', () => {
            cursor.style.opacity = '1';
        });

        // Hover states on interactive elements
        const hoverTargets = document.querySelectorAll('a, button, .emphasis, .theme-toggle');
        hoverTargets.forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
        });

        // Smooth animation loop
        function animate() {
            cursorX += (mouseX - cursorX) * 0.5;
            cursorY += (mouseY - cursorY) * 0.5;
            cursor.style.left = cursorX + 'px';
            cursor.style.top = cursorY + 'px';
            requestAnimationFrame(animate);
        }
        animate();
    }

    /* ----------------------------------------
       Loading Screen
       ---------------------------------------- */
    function initLoader() {
        const loader = document.querySelector('.loading');
        if (!loader) return;

        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.classList.add('loaded');
            }, 800);
        });
    }

    /* ----------------------------------------
       Glow Effect (follows mouse)
       ---------------------------------------- */
    function initGlow() {
        const glow = document.querySelector('.glow');
        if (!glow || window.innerWidth <= 768) return;

        document.addEventListener('mousemove', (e) => {
            const glowX = (e.pageX / window.innerWidth) * 100;
            const glowY = (e.pageY / window.innerHeight) * 100;
            const isDark = html.getAttribute('data-theme') !== 'light';
            glow.style.background = isDark
                ? `radial-gradient(circle at ${glowX}% ${glowY}%, rgba(255,255,255,0.03) 0%, transparent 60%)`
                : `radial-gradient(circle at ${glowX}% ${glowY}%, rgba(0,0,0,0.02) 0%, transparent 60%)`;
        });
    }

    /* ----------------------------------------
       Background Particles
       ---------------------------------------- */
    function initParticles() {
        const container = document.querySelector('.particles');
        if (!container) return;

        const count = 15;
        for (let i = 0; i < count; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = `${Math.random() * 100}%`;
            p.style.animationDelay = `${Math.random() * 20}s`;
            p.style.animationDuration = `${20 + Math.random() * 10}s`;
            container.appendChild(p);
        }
    }

    /* ----------------------------------------
       Konami Code Easter Egg
       ---------------------------------------- */
    function initKonami() {
        const code = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
        let index = 0;

        document.addEventListener('keydown', (e) => {
            if (e.key === code[index]) {
                index++;
                if (index === code.length) {
                    document.body.classList.add('konami-active');
                    setTimeout(() => document.body.classList.remove('konami-active'), 5000);
                    index = 0;
                }
            } else {
                index = 0;
            }
        });
    }

    /* ----------------------------------------
       Initialize everything on DOM ready
       ---------------------------------------- */
    document.addEventListener('DOMContentLoaded', () => {
        initThemeToggle();
        initCursor();
        initLoader();
        initGlow();
        initParticles();
        initKonami();
    });

})();

/* ============================================
   Global functions (used via onclick in HTML)
   ============================================ */

function showHDModal(e) {
    if (e) e.preventDefault();
    var modal = document.getElementById('hdModal');
    if (modal) modal.classList.add('active');
}

function closeHDModal() {
    var modal = document.getElementById('hdModal');
    if (modal) modal.classList.remove('active');
}
