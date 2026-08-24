(() => {
  const header = document.querySelector('[data-header]');
  const menu = document.querySelector('[data-menu]');
  const button = document.querySelector('[data-menu-button]');

  const syncHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 10);
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  button?.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    button.setAttribute('aria-expanded', String(open));
  });

  menu?.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      menu.classList.remove('is-open');
      button?.setAttribute('aria-expanded', 'false');
    }
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('[data-reveal]');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px' });
    revealItems.forEach((item, index) => {
      item.style.transitionDelay = `${Math.min(index % 4, 3) * 70}ms`;
      if (item.getBoundingClientRect().top < window.innerHeight * 0.94) {
        item.classList.add('is-visible');
      } else {
        item.classList.add('will-reveal');
        observer.observe(item);
      }
    });
  }
})();
