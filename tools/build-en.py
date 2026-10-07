#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera site/en/index.html a partir de site/index.html.

El sitio es estatico a proposito, asi que el ingles vive en su propia URL en
lugar de conmutarse con JavaScript: sale en el HTML servido, funciona sin JS y
no parpadea. Para no mantener dos archivos a mano, este script reconstruye el
ingles desde el castellano cada vez que el castellano cambia.

    python3 tools/build-en.py

Si queda castellano sin traducir, el script lo enumera y termina en error.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, "site", "index.html")
DESTINO = os.path.join(RAIZ, "site", "en", "index.html")

# Se aplican de la mas larga a la mas corta, para que una frase completa se
# traduzca antes de que una palabra suelta pueda morderla por dentro.
TEXTOS = {
    # --- cabecera del documento ---
    "Yanapuma Wildlife Sanctuary — Vida y belleza que merecen permanecer intactas":
        "Yanapuma Wildlife Sanctuary — Life and beauty that deserve to remain untouched",
    "Reserva privada de 900 hectáreas a 81 km de Santa Cruz de la Sierra, en la zona de amortiguamiento del Parque Nacional Amboró. Conservación, ecoturismo de bajo impacto y producción sostenible.":
        "A 900-hectare private reserve 81 km from Santa Cruz de la Sierra, in the buffer zone of Amboró National Park. Conservation, low-impact ecotourism and sustainable production.",
    "Yanapuma — Vida y belleza que merecen permanecer intactas":
        "Yanapuma — Life and beauty that deserve to remain untouched",
    "900 hectáreas de biodiversidad protegida junto al Parque Nacional Amboró, Bolivia.":
        "900 hectares of protected biodiversity beside Amboró National Park, Bolivia.",

    # --- interfaz ---
    "Bienvenido": "Welcome",
    "Menú": "Menu",
    "Contacto": "Contact",
    "Abrir menú": "Open menu",
    "Cerrar menú": "Close menu",
    "Principal": "Main",
    "Volver arriba": "Back to top",
    "Vuelo sobre los farallones de arenisca cubiertos de bosque":
        "Flight over the forested sandstone cliffs",

    # --- navegacion ---
    "Conservación": "Conservation",
    "Experiencias": "Experiences",
    "Estadía": "Stay",
    "Planificar una visita": "Plan a visit",

    # --- portada ---
    "Vida y belleza": "Life and beauty",
    "que merecen": "that deserve",
    "permanecer intactas": "to remain untouched",
    "Conocer Yanapuma": "Discover Yanapuma",

    # --- la reserva ---
    "Un espacio que encontró a su guardián.": "A place that found its guardian.",
    "Un compromiso": "A commitment",
    "sostenible": "sustained",
    "en el tiempo": "over time",
    "A 81 km de Santa Cruz de la Sierra, en la ruta hacia Samaipata y en la zona de amortiguamiento del Parque Nacional Amboró, Yanapuma resguarda una extraordinaria composición de paisajes, microclimas y vida silvestre.":
        "81 km from Santa Cruz de la Sierra, on the road to Samaipata and within the buffer zone of Amboró National Park, Yanapuma safeguards an extraordinary composition of landscapes, microclimates and wildlife.",
    "En las tradiciones andino-amazónicas, Yanapuma es el felino negro que habita y protege la naturaleza: una figura vinculada al equilibrio del territorio y a la idea de que el bosque merece respeto.":
        "In Andean-Amazonian tradition, Yanapuma is the black cat that inhabits and protects nature: a figure tied to the balance of the territory and to the idea that the forest deserves respect.",
    "Ese significado encontró un lugar propio en esta reserva, que nace en 2019 sobre 900 hectáreas donde paisajes, vegetación y condiciones naturales que cambian en distancias sorprendentemente cortas.":
        "That meaning found a home of its own in this reserve, born in 2019 across 900 hectares where landscapes, vegetation and natural conditions change over surprisingly short distances.",
    "Conocer la reserva": "Explore the reserve",

    # --- el modelo ---
    "Cinco dimensiones": "Five dimensions",
    "para un mismo propósito": "of a single purpose",
    "Confluencia ecológica": "Ecological confluence",
    "El territorio": "The territory",
    "Hábitats de distintas alturas que dan refugio a una biodiversidad singular.":
        "Habitats at different elevations that shelter a singular biodiversity.",
    "Zonas secas y elevadas dan paso a espacios húmedos y de vegetación densa: la variedad de microclimas permite que especies de distintos ambientes coincidan en un mismo espacio protegido.":
        "Dry, high ground gives way to humid, densely vegetated areas: the range of microclimates lets species from different environments meet within a single protected space.",
    "Yanapuma es hogar y corredor biológico del jaguar, el puma y el oso jucumari, además de una notable variedad de aves, reptiles y pequeños mamíferos.":
        "Yanapuma is home and biological corridor to the jaguar, the puma and the spectacled bear, along with a remarkable variety of birds, reptiles and small mammals.",
    "Inmersión de bajo impacto": "Low-impact immersion",
    "El acceso": "Access",
    "Senderos, miradores y avistamientos diseñados para acompañar el ritmo de la naturaleza.":
        "Trails, lookouts and sightings designed to follow nature's own pace.",
    "Cuatro senderos principales y dos trayectos cortos, adaptados a distintos niveles de caminata.":
        "Four main trails and two short routes, suited to different levels of walking.",
    "Cada visita se coordina previamente y se realiza con guías especializados. Los cupos son limitados.":
        "Every visit is arranged in advance and led by specialist guides. Places are limited.",
    "Protección activa": "Active protection",
    "La labor": "The work",
    "Recuperación del territorio y un centro dedicado a la rehabilitación de animales silvestres.":
        "Restoring the land, and a centre devoted to rehabilitating wild animals.",
    "Parte de la reserva fue impactada por actividades agrícolas; hoy se trabaja en devolver a esos suelos su cobertura vegetal nativa.":
        "Part of the reserve was affected by farming; the work today is to return native plant cover to that ground.",
    "El centro de rescate opera en alianza con las autoridades ambientales competentes.":
        "The rescue centre operates in partnership with the relevant environmental authorities.",
    "Convivencia y calma": "Coexistence and calm",
    "La estadía": "The stay",
    "Una propuesta de alojamiento exclusiva, de escala reducida, integrada al entorno.":
        "Lodging on a deliberately small scale, built into its surroundings.",
    "Construcciones con materiales locales —piedra, barro, arena y madera— orientadas para aprovechar luz y ventilación naturales.":
        "Built from local materials — stone, clay, sand and wood — and oriented to make the most of natural light and ventilation.",
    "Toda la madera proviene de árboles caídos o dañados de forma natural dentro del propio territorio.":
        "All the timber comes from trees that fell or were damaged naturally within the territory itself.",
    "Sostenibilidad en origen": "Sustainability at source",
    "La producción": "Production",
    "Café Tigrenegro, una iniciativa productiva que financia directamente la labor de Yanapuma.":
        "Café Tigrenegro, a production venture that funds Yanapuma's work directly.",
    "Como restricción autoimpuesta, Yanapuma solo puede producir sobre el 1% del total de la tierra que conserva, y únicamente en chacos antiguos, con el propósito de reforestarlos hasta alcanzar un 30% de sombra.":
        "As a self-imposed limit, Yanapuma may farm no more than 1% of the land it protects, and only on old cleared plots (chacos), with the aim of reforesting them up to 30% shade cover.",
    "Prioriza la excelencia en taza y el respeto por el suelo antes que el volumen de producción.":
        "It puts cup quality and respect for the soil ahead of volume.",
    "El complejo procesa además las cosechas de caficultores vecinos, integrando a la comunidad local al modelo.":
        "The mill also processes the harvests of neighbouring growers, bringing the local community into the model.",

    # --- conservacion ---
    "No es un zoológico.": "This is not a zoo.",
    "Es un refugio.": "It is a refuge.",
    "En alianza con las autoridades ambientales competentes, Yanapuma desarrolla un centro de rescate dedicado a animales silvestres víctimas de tráfico o pérdida de su hábitat.":
        "In partnership with the relevant environmental authorities, Yanapuma runs a rescue centre for wild animals that have been trafficked or have lost their habitat.",
    "Cada individuo recibe evaluación médica y cuidados especializados, en procura de una eventual reintroducción en su hábitat natural cuando sea biológicamente viable.":
        "Each animal receives medical assessment and specialist care, working towards eventual reintroduction into its natural habitat whenever that is biologically viable.",
    "Cuando no lo es, la prioridad es garantizar un refugio permanente, con recintos diseñados bajo criterios de bienestar y enriquecimiento ambiental. No es un espacio de exhibición.":
        "When it is not, the priority is a permanent refuge, in enclosures designed around welfare and environmental enrichment. This is not a place of exhibition.",
    "Cómo trabaja el centro": "How the centre works",

    # --- restauracion ---
    "Restauración": "Restoration",
    "Veinte hectáreas": "Twenty hectares",
    "que vuelven al bosque": "returning to forest",
    "El proyecto abarca 1.100 hectáreas distribuidas en dos propiedades: Volcanes y Piedras Blancas.":
        "The project covers 1,100 hectares across two properties: Volcanes and Piedras Blancas.",
    "Veinte de esas hectáreas están deforestadas y hoy se encuentran en proceso de restauración. El objetivo es devolverles cobertura boscosa hasta que vuelvan a integrarse al bosque que las rodea.":
        "Twenty of those hectares were deforested and are now being restored. The aim is to bring back forest cover until they rejoin the woodland around them.",
    "1.100 ha": "1,100 ha",
    "Superficie del proyecto": "Project area",
    "En restauración": "Under restoration",
    "Donar a la reforestación": "Donate to the reforestation",

    # --- aves ---
    "Observación de aves": "Birdwatching",
    "Un territorio": "A territory",
    "para observadores": "for birders",
    "La topografía de montaña, sin planicies, facilita encontrar y seguir a las aves. Cada zona de la reserva ofrece algo distinto según la hora del día.":
        "Mountain topography, with no flat ground, makes birds easier to find and follow. Each part of the reserve offers something different depending on the time of day.",
    "Mirador": "Lookout",
    "Rapaces, entre ellas el Águila Arpía, además de colibríes y tangaras durante la mañana.":
        "Raptors, including the Harpy Eagle, plus hummingbirds and tanagers through the morning.",
    "Camino a la cascada": "Trail to the waterfall",
    "Pavas de monte y tinamúes. También grupos de monos capuchinos, poco esquivos.":
        "Guans and tinamous. Also troops of capuchin monkeys, not especially shy.",
    "Toma de agua": "Water intake",
    "Recorrido nocturno: hasta seis especies de búhos.":
        "A night walk: up to six owl species.",
    "Camino de llegada": "Access road",
    "Terreno plano, bueno para atrapamoscas y bandadas mixtas de alto dosel.":
        "Flat ground, good for flycatchers and mixed canopy flocks.",
    "Entre las más buscadas": "Among the most sought after",
    "Búhos registrados en la reserva": "Owls recorded in the reserve",
    "Especies registradas": "Species recorded",
    "Listas subidas": "Checklists submitted",
    "Cifras del hotspot ": "Figures from the ",
    " en eBird; la reserva tiene además otros puntos registrados. Allí el Buff-fronted Owl aparece 231 veces más frecuente que la media de la región. Relevamiento de campo de Raúl Navi, guía de observación de aves.":
        " hotspot on eBird; the reserve has other registered points as well. There the Buff-fronted Owl is 231 times more frequent than the regional average. Field survey by Raúl Navi, birding guide.",
    "Ver el hotspot en eBird": "View the hotspot on eBird",
    "Foto pendiente": "Photo coming soon",
    "Foto: ": "Photo: ",

    # --- como se financia ---
    "El modelo sigue creciendo.": "The model keeps growing.",
    "Cómo se financia": "How conservation",
    "la conservación": "is funded",
    "Auspicio de cámaras trampa": "Camera trap sponsorship",
    "Auspicia una cámara trampa de la reserva. Cada mes te compartimos las imágenes que registró: quién pasó por ahí y a qué hora.":
        "Sponsor one of the reserve's camera traps. Each month we share the images it recorded: who passed by, and at what hour.",
    "Aporte mensual": "Monthly contribution",
    "Tours guiados": "Guided tours",
    "Recorridos por senderos, cascadas y miradores, siempre acompañados por personal de la reserva y con cupos limitados.":
        "Walks along trails, waterfalls and lookouts, always accompanied by reserve staff and with limited places.",
    "Con reserva previa": "By prior booking",
    "Compra de café": "Coffee purchase",
    "Café Tigrenegro, cultivado bajo sombra dentro de la reserva. El beneficio se destina directamente al resguardo del territorio.":
        "Café Tigrenegro, grown under shade inside the reserve. The proceeds go directly to protecting the territory.",
    "Compra directa": "Direct purchase",
    "Voluntariados": "Volunteering",
    "Estancias de trabajo junto al equipo, en tareas de conservación, reforestación y apoyo al centro de rescate.":
        "Working stays alongside the team, on conservation, reforestation and support for the rescue centre.",
    "Estancias coordinadas": "Arranged stays",
    "Auspicio de animales rescatados": "Rescued animal sponsorship",
    "Auspicia a un animal del centro de rescate y recibe cada mes un informe de cómo avanza su recuperación y su enriquecimiento.":
        "Sponsor an animal at the rescue centre and receive a monthly report on how its recovery and enrichment are progressing.",
    "Consultar sobre el aporte mensual": "Ask about the monthly contribution",
    "Registro de una cámara trampa de la reserva": "Footage from one of the reserve's camera traps",
    "Ver los tours": "See the tours",
    "Sobre el café": "About the coffee",
    "Consultar sobre el voluntariado": "Ask about volunteering",
    "Consultar sobre aportes": "Ask about contributions",

    # --- marquesina ---
    "Jaguar · Puma · Oso jucumari · Aves · Reptiles · Pequeños mamíferos · Bosque nublado · Microclimas ·":
        "Jaguar · Puma · Spectacled bear · Birds · Reptiles · Small mammals · Cloud forest · Microclimates ·",

    # --- experiencias ---
    "Vivir la naturaleza": "Living nature",
    "y su calma": "and its calm",
    "Sendero Cascada Flor de Oro": "Flor de Oro Waterfall Trail",
    "Descender hacia cascadas escondidas y pozas flanqueadas por paredones de piedra.":
        "Descending to hidden waterfalls and pools flanked by walls of stone.",
    "Sendero Parque Amboró Zona Norte": "Amboró Park North Zone Trail",
    "Aquí la fauna habita en libertad: los avistamientos no se fuerzan, se descubren con paciencia y silencio.":
        "Here wildlife lives free: sightings are not staged, they are found with patience and silence.",
    "Sendero Mataracú": "Mataracú Trail",
    "Aproximarse a la zona de Volcanes y a los cafetales bajo sombra de la reserva.":
        "Getting close to the Volcanes area and the reserve's shade-grown coffee.",
    "Ver imágenes": "See images",
    "Cerrar galería": "Close gallery",
    "Foto anterior": "Previous photo",
    "Foto siguiente": "Next photo",

    # --- estadia ---
    "Habitar la reserva": "Inhabiting the reserve",
    "a un ritmo pausado": "at an unhurried pace",
    "Las construcciones priorizan materiales locales —piedra, barro, arena y madera— y aprovechan la luz y la ventilación natural sin romper la serenidad del paisaje.":
        "The buildings favour local materials — stone, clay, sand and wood — and draw on natural light and ventilation without disturbing the calm of the landscape.",
    "Toda la madera empleada proviene de árboles caídos o dañados de forma natural dentro del propio territorio.":
        "All the timber used comes from trees that fell or were damaged naturally within the territory itself.",
    "Para proteger la tranquilidad del ecosistema, la capacidad se mantiene acotada: la primera cabaña cuenta con dos habitaciones independientes con baño privado y capacidad máxima de seis personas.":
        "To protect the quiet of the ecosystem, capacity is kept small: the first cabin has two independent rooms with private bathrooms and sleeps a maximum of six.",
    "Consultar disponibilidad": "Check availability",

    # --- cafe ---
    "Del bosque recuperado": "From recovered forest",
    "a la taza": "to the cup",
    "Al jaguar se lo llama tigre. En la leyenda del Yanapuma su nombre va a veces precedido de Tigrenegro: dos maneras de decir lo mismo. De ahí lo toma el café de la reserva.":
        "The jaguar is colloquially called a tiger. In the Yanapuma legend its name is sometimes preceded by Tigrenegro, black tiger: two ways of saying the same thing. That is where the reserve's coffee takes its name.",
    "El café nació de la conservación, no al revés. Del bosque a la taza. 1% cultivado 99% conservado.":
        "The coffee was born of conservation, not the other way round. From forest to cup. 1% cultivated, 99% conserved.",
    "Centro de Rescate.": "Rescue Centre.",
    "El café nació de la conservación, no al revés. Para recuperar los terrenos desmontados había que volver a plantarlos, y el cultivo bajo sombra permitió hacerlo produciendo.":
        "The coffee grew out of the conservation work, not the other way round. Recovering the cleared ground meant planting it again, and growing under shade made it possible to do that productively.",
    "Los cafetales crecen entre los 1.400 y los 1.750 metros, en suelos de terroirs distintos. La reserva cuenta con centro de beneficio propio y un banco genético de variedades exóticas de alto potencial en taza.":
        "The groves grow between 1,400 and 1,750 metres, in soils of different terroirs. The reserve has its own processing mill and a genetic bank of exotic varieties with high cup potential.",
    "Consultar por el café": "Ask about the coffee",

    # --- mapa ---
    "Sobre la ruta hacia Samaipata.": "On the road to Samaipata.",
    "A 81 km de Santa&nbsp;Cruz de la Sierra": "81 km from Santa&nbsp;Cruz de la Sierra",
    "Yanapuma se encuentra en un entorno vinculado al Parque Nacional Amboró. Para proteger la experiencia y preparar adecuadamente cada visita, el ingreso debe coordinarse previamente.":
        "Yanapuma sits in a setting tied to Amboró National Park. To protect the experience and prepare each visit properly, entry must be arranged in advance.",
    "Coordinar visita": "Arrange a visit",

    # --- pie ---
    "Proteger la naturaleza también es aprender a estar en ella sin dejar huella.":
        "Protecting nature also means learning to be in it without leaving a trace.",
    "Ruta a Samaipata, km 81": "Samaipata road, km 81",
    "Escribir ahora": "Message us",
    "Correo": "Email",
    "Formulario de consulta": "Enquiry form",
    "Redes": "Social",

    # --- textos alternativos ---
    "Vista aérea del valle y los farallones de arenisca de la reserva":
        "Aerial view of the valley and the reserve's sandstone cliffs",
    "Sendero de altura con vista sobre las serranías":
        "High trail looking out over the ranges",
    "Registro de cámara trampa: un puma recorre el sotobosque":
        "Camera trap record: a puma moves through the understorey",
    "Galería de madera abierta con vista al valle":
        "Open timber veranda looking over the valley",
    "Cafetal cultivado bajo sombra con las serranías al fondo":
        "Shade-grown coffee with the ranges behind",
    "Equipo de la reserva trasladando plantines para reforestación":
        "Reserve team moving seedlings for reforestation",
    "Cascada cayendo sobre una poza de aguas claras":
        "A waterfall dropping into a clear pool",
    "Cielo abierto sobre las serranías boscosas":
        "Open sky over the forested ranges",
    "Café recién preparado sirviéndose humeante en una taza":
        "Freshly brewed coffee being poured, steaming, into a cup",
    "Mapa del Parque Nacional Amboró entre Cochabamba y Santa Cruz, con la ruta que pasa por Samaipata y los predios de Yanapuma en Volcanes y Piedras Blancas":
        "Map of Amboró National Park between Cochabamba and Santa Cruz, with the road through Samaipata and Yanapuma's Volcanes and Piedras Blancas properties",
    "mapa-amboro.svg?v=": "mapa-amboro-en.svg?v=",
    "Video de ejemplo, solo como referencia": "Sample video, for reference only",
}

# Bloques que solo tienen sentido en castellano.
FUERA = [
    '\n          <p class="note">Los nombres se mantienen en inglés, que es como se '
    'catalogan y buscan internacionalmente.</p>',
]


def construir(html):
    for bloque in FUERA:
        if bloque not in html:
            sys.exit("No encuentro el bloque a quitar:\n  " + bloque[:70])
        html = html.replace(bloque, "")

    for es, en in sorted(TEXTOS.items(), key=lambda par: -len(par[0])):
        html = html.replace(es, en)

    # La pagina vive un nivel mas abajo, asi que los recursos suben uno.
    html = re.sub(r'(href|src|content|poster)="(css/|js/|assets/)', r'\1="../\2', html)

    # Idioma del documento y del grafo abierto.
    html = html.replace('<html lang="es">', '<html lang="en">', 1)
    html = html.replace('content="es_BO"', 'content="en"', 1)

    # El selector de idioma y los alternos apuntan al reves. Sin contador: el
    # selector sale dos veces, en el menu y en el pie.
    html = html.replace('<a href="./" hreflang="es" aria-current="true">ES</a>',
                        '<a href="../" hreflang="es">ES</a>')
    html = html.replace('<a href="en/" hreflang="en">EN</a>',
                        '<a href="./" hreflang="en" aria-current="true">EN</a>')
    html = html.replace('<link rel="alternate" hreflang="es" href="./">',
                        '<link rel="alternate" hreflang="es" href="../">', 1)
    html = html.replace('<link rel="alternate" hreflang="en" href="en/">',
                        '<link rel="alternate" hreflang="en" href="./">', 1)
    html = html.replace('<link rel="alternate" hreflang="x-default" href="./">',
                        '<link rel="alternate" hreflang="x-default" href="../">', 1)
    return html


def sobras(html):
    """Texto visible que sigue en castellano, para no publicar a medias."""
    sin_svg = re.sub(r"<svg.*?</svg>", "", html, flags=re.S)
    sin_script = re.sub(r"<script.*?</script>", "", sin_svg, flags=re.S)
    trozos = [t.strip() for t in re.split(r"<[^>]+>", sin_script) if t.strip()]
    trozos += re.findall(r'(?:alt|aria-label|content)="([^"]*)"', sin_script)
    pista = re.compile(
        r"[áéíóúñ¿¡]"
        r"|\b(?:de|la|el|los|las|con|para|que|una|del|por|y|en)\b",
        re.I)
    guardar = ("Yanapuma", "Ambor", "Samaipata", "Santa Cruz", "Santa&nbsp;Cruz",
               "Tigrenegro", "Flor de Oro", "Mataracú",
               "Bolivia", "Volcanes", "Piedras Blancas", "Navi", "eBird",
               "Owl", "Recurvebill", "Tapaculo", "Gnateater", "Toucanet",
               "Racket-tail", "terroir")
    # Menos de cuatro letras no da para decidir el idioma: "EN", "es", "ha".
    return [t for t in trozos
            if len(t) > 3 and pista.search(t)
            and not any(g in t for g in guardar)]


def main():
    html = io.open(ORIGEN, encoding="utf-8").read()
    salida = construir(html)

    pendiente = sobras(salida)
    if pendiente:
        print("Castellano sin traducir (%d):" % len(pendiente))
        for t in pendiente:
            print("  ·", t[:110])
        sys.exit(1)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    io.open(DESTINO, "w", encoding="utf-8").write(salida)
    print("Escrito %s (%d KB)" % (
        os.path.relpath(DESTINO, RAIZ), len(salida.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
