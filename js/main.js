/* Yanapuma — Versión B. Sin dependencias. */
(function () {
  'use strict';

  /* ---------- Pantalla de bienvenida ---------- */
  var pl = document.getElementById('preloader');
  if (pl) {
    var root = document.documentElement;

    if (root.classList.contains('pl-seen')) {
      pl.remove();                       // ya la vio: fuera del DOM
    } else {
      document.body.classList.add('pl-lock');

      // Escalonado del centro hacia afuera: la cara se arma desde el hocico.
      // A cada forma le calculamos de donde viene: sale despedida en la direccion
      // radial en la que vive dentro del rostro, asi que al volver todo converge.
      var svg = pl.querySelector('svg');
      var shapes = [].slice.call(pl.querySelectorAll('path,polygon'));
      var vb = svg.viewBox.baseVal;
      var cx = vb.width / 2, cy = vb.height / 2;

      shapes.map(function (el) {
        var b;
        try { b = el.getBBox(); } catch (e) { b = { x: cx, y: cy, width: 0, height: 0 }; }
        var dx = (b.x + b.width / 2) - cx, dy = (b.y + b.height / 2) - cy;
        return { el: el, dx: dx, dy: dy, d: Math.sqrt(dx * dx + dy * dy) };
      }).sort(function (a, b) {
        return a.d - b.d;
      }).forEach(function (o, i) {
        var st = o.el.style;
        st.setProperty('--i', i);

        // Direccion de entrada. Las longitudes en px de un transform SVG son
        // unidades del viewBox (222 x 279), no pixeles de pantalla.
        var ux = o.d ? o.dx / o.d : 0;
        var uy = o.d ? o.dy / o.d : -1;          // el centro exacto baja desde arriba
        var vaiven = 0.85 + ((i * 37) % 21) / 52.5;   // 0.85 - 1.23, determinista
        var lejos = (220 + o.d * 1.2) * vaiven;       // la orilla viene de mas lejos

        st.setProperty('--dx', (ux * lejos).toFixed(1) + 'px');
        st.setProperty('--dy', (uy * lejos).toFixed(1) + 'px');
        st.setProperty('--rot', ((i % 2 ? 1 : -1) * (12 + (i % 7) * 4)) + 'deg');
      });

      var minDone = false, loadDone = false, cerrada = false;

      function cerrar() {
        if (cerrada || !minDone || !loadDone) return;
        cerrada = true;
        root.classList.add('pl-done');
        document.body.classList.remove('pl-lock');
        try { localStorage.setItem('yanapuma.welcomed', '1'); } catch (e) {}
        setTimeout(function () { pl.remove(); }, 700);
      }

      setTimeout(function () { minDone = true; cerrar(); }, 2500);
      if (document.readyState === 'complete') { loadDone = true; cerrar(); }
      else window.addEventListener('load', function () { loadDone = true; cerrar(); });

      // Salvavidas: si algun recurso nunca termina, no dejamos la pagina tapada.
      setTimeout(function () { minDone = loadDone = true; cerrar(); }, 6000);
    }
  }

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

  /* Aves: cada grupo muestra la foto de la especie elegida */
  Array.prototype.forEach.call(document.querySelectorAll('.bird-pick'), function (g) {
    var fig = g.querySelector('.bird-ph'), img = fig.querySelector('img'),
        cred = fig.querySelector('figcaption a'),
        bs = Array.prototype.slice.call(g.querySelectorAll('button'));
    bs.forEach(function (b) {
      b.addEventListener('click', function () {
        bs.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        var src = b.getAttribute('data-src');
        fig.classList.toggle('is-empty', !src);
        img.hidden = cred.hidden = !src;
        if (!src) return;
        img.src = src;
        img.alt = b.textContent;
        cred.href = b.getAttribute('data-href');
        cred.textContent = b.getAttribute('data-credit');
      });
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
