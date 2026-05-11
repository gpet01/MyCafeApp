//  Nav on Scroll 
const nav = document.getElementById('nav');

window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
});

//  Scroll Reveal 
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── Highlight Today's Hours ──
const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const today = days[new Date().getDay()];

document.querySelectorAll('.day[data-day]').forEach(el => {
  if (el.dataset.day === today) {
    el.classList.add('today');
    el.textContent = today + ' — Today';
    el.nextElementSibling.classList.add('today');
  }
});

// - Loading top page after reset

window.onbeforeunload = () => {
    window.scrollTo(0,0);
};

// Hamburger functionallity //
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navLinks.classList.toggle('open');
});

document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinks.classList.remove('open');
  })
});

// Menu filter buttonss //
const filterButtons = document.querySelectorAll('.filter-btn');
const menuSections = document.querySelectorAll('.menu-section');

filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    //Εδω αφαιρω το active απο ολα τα κουμπια
    filterButtons.forEach(b => b.classList.remove('active'));
    //Εδω προσθετω το active στο κουμπι που πατησα
    btn.classList.add('active');

    const filter = btn.dataset.filter;

    menuSections.forEach(section => {
      if (filter === 'all' || section.dataset.section === filter) {
        section.style.display = 'block';
      } else {
        section.style.display = 'none';
      }
    });
  });
})
