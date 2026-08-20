# Método Adiestramiento Canino — landing

Landing estática de un solo archivo (`index.html`). Sin build, sin dependencias.
En Vercel: importar el repo y desplegar como *Other / Static*. No hace falta configurar nada.

## Qué hay que configurar antes de publicar

**Los 3 links de checkout.** Hoy los tres apuntan a `/checkout`. En `index.html`, buscá
`data-link=` y poné la URL del producto que corresponda:

| Plan | Precio | Clases |
|---|---|---|
| Básico | AR$ 14.900 | 18 |
| Completo *(preseleccionado)* | AR$ 23.900 | 31 |
| Avanzado | AR$ 28.900 | 36 |

**El pixel de Meta.** No está incluido. Si la landing va a recibir tráfico pago, hay que
pegar el snippet antes de `</head>` y disparar `InitiateCheckout` en el click del CTA.

## Cómo está armada

- Un solo HTML: CSS y JS embebidos, sin librerías externas más allá de Google Fonts.
- Las miniaturas y el clip del hero salen del bucket público de Supabase
  (`algoritmia-img/adiestramiento-canino/`).
- Los 3 planes aparecen en el hero, arriba de todo. El del medio viene preseleccionado
  y los dos selectores (hero y cierre) están sincronizados: si cambiás uno, cambia el otro
  y también el botón flotante.
- Responsive verificado en 390 / 768 / 1280 px: sin scroll horizontal, sin imágenes rotas
  y sin errores de JavaScript.

## Para regenerarla

El HTML lo escupe `build_landing.py`, que lee las duraciones reales de los videos y arma
el temario solo. Si cambian las clases o los precios, se edita ahí y se vuelve a generar.
