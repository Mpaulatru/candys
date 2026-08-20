# ClaroVenta – Prototipo UX/UI

Aplicación web para dueños de pequeños negocios que quieren entender qué productos les generan (o les quitan) dinero.

## Estructura del proyecto

```
claroventa/
├── index.html          → Landing page
├── upload.html         → Carga de datos (CSV + manual)
├── dashboard.html      → Dashboard principal
├── product.html        → Detalle de un producto
├── css/
│   └── styles.css      → Sistema de diseño + estilos custom
├── js/
│   └── app.js          → Interacciones (upload, tabs, menú, etc.)
├── server.py           → Servidor de desarrollo
└── README.md
```

## Cómo verlo

```bash
cd claroventa
python server.py
```

Luego abre: **http://localhost:8000**

## Páginas

| Página        | Archivo           | Descripción                              |
|---------------|-------------------|------------------------------------------|
| Landing       | `index.html`      | Página pública de inicio                 |
| Cargar datos  | `upload.html`     | Subir CSV o carga manual                 |
| Dashboard     | `dashboard.html`  | Resumen + alertas + recomendaciones      |
| Producto      | `product.html`    | Detalle + gráfico + acciones específicas |

## Stack

- HTML5 semántico
- Tailwind CSS (CDN)
- CSS custom (`styles.css`)
- JavaScript vanilla (`app.js`)
- Lucide Icons
- Tipografía: Inter

## Diseño

Estilo **Linear + Notion + Stripe**: limpio, profesional, mucho espacio en blanco, fácil de usar para personas de 40-60 años.
