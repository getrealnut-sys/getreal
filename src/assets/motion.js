/* Scroll work for motion.css. Does nothing when <html> has no m-* classes (reduced motion). */
(function () {
  var h = document.documentElement, on = function (c) { return h.classList.contains(c); };
  if (!/\bm-/.test(h.className)) return;
  var bar = document.createElement('div'); bar.id = 'm-bar'; document.body.appendChild(bar);
  var header = document.querySelector('header');
  var hero = document.querySelector('section');
  var art = hero && hero.querySelector('svg.art-in'); art = art && art.parentElement;
  if (art) art.classList.add('m-par');

  // stagger: siblings inside the same grid or row get increasing delays
  var groups = new Map();
  document.querySelectorAll('.rv').forEach(function (el) {
    var p = el.parentElement, n = groups.get(p) || 0; groups.set(p, n + 1);
    el.classList.add('m-st'); el.style.transitionDelay = (Math.min(n % 4, 3) * 0.18) + 's';
  });
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('m-on'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px' }) : null;
  document.querySelectorAll('.m-st').forEach(function (el) { io ? io.observe(el) : el.classList.add('m-on'); });

  var tick = function () {
    var y = window.scrollY || 0, max = (document.documentElement.scrollHeight - window.innerHeight) || 1;
    bar.style.transform = 'scaleX(' + Math.min(1, y / max) + ')';
    if (art) art.style.transform = on('m-parallax') && y < window.innerHeight * 1.5 ? 'translateY(' + (y * 0.35) + 'px)' : '';
    if (header) header.classList.toggle('m-slim', y > 60);
  };
  var queued = false;
  window.addEventListener('scroll', function () { if (!queued) { queued = true; requestAnimationFrame(function () { queued = false; tick(); }); } }, { passive: true });
  window.addEventListener('resize', tick); h.addEventListener('m-change', tick); tick();

  // soft page fades on links to other pages of the site
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || !on('m-fade') || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var href = a.getAttribute('href');
    if (!href || /^(https?:|mailto:|#)/.test(href) || href.indexOf('#') > 0 && a.pathname === location.pathname) return;
    e.preventDefault(); document.body.classList.add('m-out');
    setTimeout(function () { location.href = a.href; }, 300);
  });
  window.addEventListener('pageshow', function () { document.body.classList.remove('m-out'); });
})();
