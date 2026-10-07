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

  /* Experiencias: cada sendero abre su galería en una ventana modal.
     Las fotos viven en el <template class="gal-fotos"> de cada tarjeta;
     data-src vacío muestra el aviso de foto pendiente, como en las aves. */
  (function () {
    var dlg = document.getElementById('galeria');
    if (!dlg || typeof dlg.showModal !== 'function') return;
    var titulo = dlg.querySelector('.gal-t'),
        pista = dlg.querySelector('.gal-track'),
        escena = dlg.querySelector('.gal-stage'),
        cuenta = dlg.querySelector('.gal-n'),
        nav = dlg.querySelector('.gal-nav'),
        vacio = dlg.querySelector('.gal-vacio'),
        fotos = [], i = 0, origen = null, abajo = null, x0 = null;

    function ir(n) {
      i = (n + fotos.length) % fotos.length;
      pista.style.transform = 'translateX(' + (-100 * i) + '%)';
      fotos.forEach(function (f, k) { f.setAttribute('aria-hidden', String(k !== i)); });
      cuenta.textContent = (i + 1) + ' / ' + fotos.length;
    }

    function abrir(b) {
      var card = b.closest('article'),
          items = [].slice.call(card.querySelector('.gal-fotos').content.querySelectorAll('img'));
      if (!items.length) items = [null];
      titulo.textContent = card.querySelector('h3').textContent;
      pista.innerHTML = '';
      fotos = items.map(function (it) {
        var fig = document.createElement('figure'),
            src = it && it.getAttribute('data-src');
        fig.className = 'gal-sl';
        if (src) {
          var img = document.createElement('img');
          img.src = src;
          img.alt = it.alt;
          img.draggable = false;
          fig.appendChild(img);
        } else {
          fig.appendChild(vacio.content.cloneNode(true));
        }
        pista.appendChild(fig);
        return fig;
      });
      nav.hidden = fotos.length < 2;
      ir(0);                      // con la ventana cerrada no hay transición: abre en la primera
      origen = b;
      document.body.classList.add('locked');
      dlg.showModal();
    }

    [].forEach.call(document.querySelectorAll('.js-gal'), function (b) {
      b.addEventListener('click', function () { abrir(b); });
    });
    dlg.querySelector('.gal-x').addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.gal-prev').addEventListener('click', function () { ir(i - 1); });
    dlg.querySelector('.gal-next').addEventListener('click', function () { ir(i + 1); });
    dlg.addEventListener('close', function () {
      document.body.classList.remove('locked');
      if (origen) origen.focus();
    });

    // Clic en el velo: solo si el gesto empezó y terminó fuera de la foto,
    // para que un arrastre que se escapa del encuadre no cierre la ventana.
    dlg.addEventListener('pointerdown', function (e) { abajo = e.target; });
    dlg.addEventListener('click', function (e) {
      if (e.target === dlg && abajo === dlg) dlg.close();
    });

    dlg.addEventListener('keydown', function (e) {
      if (fotos.length < 2) return;
      if (e.key === 'ArrowRight') ir(i + 1);
      else if (e.key === 'ArrowLeft') ir(i - 1);
    });

    // Deslizar con el dedo (o arrastrar con el ratón) cambia de foto.
    escena.addEventListener('pointerdown', function (e) { x0 = e.clientX; });
    escena.addEventListener('pointercancel', function () { x0 = null; });
    escena.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0;
      x0 = null;
      if (fotos.length > 1 && Math.abs(dx) > 40) ir(i + (dx < 0 ? 1 : -1));
    });
  })();

  /* Marquesina: se duplica el contenido para que el bucle no corte */
  var track = document.querySelector('.marquee-t');
  if (track) track.innerHTML += track.innerHTML;

  /* Video: respetar reducción de movimiento */
  var v = document.querySelector('.hero-b video');
  if (v && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    v.removeAttribute('autoplay'); v.pause();
  }
})();
