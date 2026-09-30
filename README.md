# Yanapuma Wildlife Sanctuary — Home

Página de inicio para **Yanapuma Wildlife Sanctuary**, reserva privada de
conservación en la zona de amortiguamiento del Parque Nacional Amboró
(Santa Cruz, Bolivia).

**Vista publicada:** https://giro54bo.github.io/yanapuma-web/

De las dos direcciones que se presentaron, el cliente eligió la opción B. Es la
que vive en este repositorio; la opción A se retiró.

## Stack

HTML, CSS y JavaScript puros. Sin framework, sin dependencias, sin proceso de
build. La única petición externa es Google Fonts.

```
index.html    La home completa
css/          styles.css
js/           main.js
assets/       img · svg · video
```

## Secciones

La Reserva · El Modelo · Conservación (con el bloque de Restauración) ·
Observación de aves · Cómo se financia la conservación · Experiencias ·
Estadía · Café Tigre Negro · Cómo llegar

## Notas

- **Pantalla de bienvenida.** En la primera visita el isotipo se arma pieza por
  pieza sobre fondo olivo. Queda registrada en `localStorage`
  (`yanapuma.welcomed`); borrar esa clave la vuelve a mostrar.
- **Tipografía.** Archivo en todo el sitio. Arima Madurai queda reservada para
  el logotipo.
- **Color.** Verde olivo `#424530` y naranja `#E09132`, con sus neutros
  derivados.
- **Pendiente de contenido.** Montos de auspicio, número de cámaras trampa, qué
  animales admiten auspicio y las condiciones de los voluntariados. El botón de
  donación a la reforestación lleva a contacto: la primera versión no incluye
  pasarela de pago.

---

Desarrollo: [Giro54](https://github.com/Giro54BO)
