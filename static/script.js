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