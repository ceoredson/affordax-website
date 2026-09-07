(() => {
  document.querySelector('[data-error-summary]')?.focus();
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

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.classList.contains('is-open')) {
      menu.classList.remove('is-open');
      button?.setAttribute('aria-expanded', 'false');
      button?.focus();
    }
  });

  document.querySelectorAll('[data-product-tour]').forEach((tour) => {
    const tabs = [...tour.querySelectorAll('[data-tour-tab]')];
    const panels = [...tour.querySelectorAll('[data-tour-panel]')];
    const tablist = tour.querySelector('[data-tour-tabs]');
    tablist.hidden = false;
    tablist.setAttribute('role', 'tablist');
    const activate = (selected, focus = false) => {
      tabs.forEach((tab, index) => {
        const active = index === selected;
        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', String(active));
        tab.setAttribute('aria-controls', tab.dataset.tourTab);
        tab.tabIndex = active ? 0 : -1;
        panels[index].hidden = !active;
        panels[index].setAttribute('role', 'tabpanel');
        panels[index].setAttribute('aria-labelledby', tab.id);
        panels[index].tabIndex = 0;
      });
      if (focus) tabs[selected].focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(index));
      tab.addEventListener('keydown', (event) => {
        let selected = index;
        if (event.key === 'ArrowRight') selected = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') selected = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') selected = 0;
        else if (event.key === 'End') selected = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(selected, true);
      });
    });
    activate(0);
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
