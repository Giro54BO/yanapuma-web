# Yanapuma — Propuestas de diseño web

Dos direcciones de diseño para la home de **Yanapuma Wildlife Sanctuary**, reserva
privada de conservación en la zona de amortiguamiento del Parque Nacional Amboró
(Santa Cruz, Bolivia).

| | Archivo | Carácter |
|---|---|---|
| **Opción A** | [`index.html`](index.html) | Editorial y ordenada. Cabecera fija, pilares en rejilla, bloques imagen + texto. |
| **Opción B** | [`index-b.html`](index-b.html) | Inmersiva. Riel lateral fijo, hero a pantalla completa, divisores ondulados, lista numerada y marquesina. |

## Stack

HTML, CSS y JavaScript puros. Sin framework, sin dependencias, sin proceso de build.
La única petición externa es Google Fonts.

```
index.html        Opción A
index-b.html      Opción B
css/              styles.css (A) · styles-b.css (B)
js/               main.js (A) · main-b.js (B)
assets/           img · video · svg
```

## Marca

- **Paleta:** Verde Olivo `#424530` y Naranja `#E09132`, más neutros derivados.
- **Tipografía:** Arima Madurai (titulares) + Archivo (texto).

## Ver en local

```bash
python3 -m http.server 4173
```

Luego abrir <http://localhost:4173/index.html> o <http://localhost:4173/index-b.html>.

---

Trabajo de [Giro54](https://github.com/Giro54BO). Contenido y material gráfico
propiedad de Yanapuma Wildlife Sanctuary.
