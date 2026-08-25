/* Yanapuma — Versión B. Sin dependencias. */
(function () {
  'use strict';

  /* Menú a pantalla completa */
  var open = document.querySelector('.rail .js-menu'),
      close = document.querySelector('.menu-x'),
      panel = document.querySelector('.menu-o');

  function setMenu(v) {
    panel.classList.toggle('open', v);
    document.body.classList.toggle('locked', v);
    if (open) open.setAttribute('aria-expanded', String(v));
    if (v) { var f = panel.querySelector('a'); if (f) f.focus(); }
    else if (open) open.focus();
  }
  if (open && panel) {
    open.addEventListener('click', function () { setMenu(true); });
    if (close) close.addEventListener('click', function () { setMenu(false); });
    panel.addEventListener('click', function (e) { if (e.target.tagName === 'A') setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('open')) setMenu(false);
    });
  }

  /* Lista numerada en acordeón */
  var btns = Array.prototype.slice.call(document.querySelectorAll('.step-b'));
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var isOpen = b.getAttribute('aria-expanded') === 'true';
      btns.forEach(function (o) {
        o.setAttribute('aria-expanded', 'false');
        document.getElementById(o.getAttribute('aria-controls')).hidden = true;
      });
      if (!isOpen) {
        b.setAttribute('aria-expanded', 'true');
        document.getElementById(b.getAttribute('aria-controls')).hidden = false;
      }
    });
  });

  /* Marquesina: se duplica el contenido para que el bucle no corte */
  var track = document.querySelector('.marquee-t');
  if (track) track.innerHTML += track.innerHTML;

  /* Video: respetar reducción de movimiento */
  var v = document.querySelector('.hero-b video');
  if (v && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    v.removeAttribute('autoplay'); v.pause();
  }
})();
