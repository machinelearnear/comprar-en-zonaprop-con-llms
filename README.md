# Mucho machine learning con Zonaprop y con Airbnb
- https://www.machinelearnear.com/
- https://www.youtube.com/@machinelearnear

![youtube_thumbnail_machinelearnear (11) copy](https://github.com/machinelearnear/comprar-en-zonaprop-con-llms/assets/78419164/942ed8a8-8f89-4b63-9138-c519d634c4a8)

Este proyecto se centra en el análisis exhaustivo de listados de propiedades de Airbnb y Zonaprop, específicamente en la zona de Buenos Aires. Usamos modelos de machine learning y técnicas avanzadas de análisis de datos para extraer insights valiosos que podrían ayudar tanto a compradores como a vendedores en el mercado inmobiliario.

Nota: Todo este `README.md` obviamente esta generado con un LLM 🤡

## Estructura del Proyecto
```sh
.
├── 01-inside-airbnb-data.ipynb
├── 02-scrape-zonaprop-listings.ipynb
├── 03-load-data-and-run.ipynb
├── LICENSE
├── README.md
├── environment.yml
├── notebooks
│ ├── 00-analyse-information.ipynb
│ └── 00-hotel-listings-in-booking.ipynb
├── processed
│ ├── airbnb_listings.csv
│ ├── airbnb_reviews.csv
│ ├── inmuebles-venta-barrio-norte-palermo-colegiales-villa-crespo-publicado-hace-menos-de-45-dias-50000-130000-dolar-orden-visitas-descendente
│ │ ├── zonaprop_listings.csv
│ │ └── zonaprop_with_userviews.csv
│ └── inmuebles-venta-palermo-colegiales-villa-crespo-chacarita-con-balcon-y-disposicion-frente-mas-30-m2-cubiertos-50000-130000-dolar
│ ├── zonaprop_listings.csv
│ └── zonaprop_with_userviews.csv
├── raw_data
│ ├── airbnb
│ │ ├── calendar_full.csv
│ │ ├── listings.csv
│ │ ├── listings_full.csv
│ │ ├── neighbourhoods.csv
│ │ ├── neighbourhoods.geojson
│ │ ├── reviews.csv
│ │ └── reviews_full.csv
│ └── zonaprop
│ ├── listings-001.html
│ ├── listings-002.html
│ ...
│ └── listings-075.html
└── webapp-work-in-progress.ipynb
```


## Para arrancar rápido

1. **environment**: Para instalar todas las dependencias necesarias, usá el archivo `environment.yml` con Conda:

    ```bash
    conda env create -f environment.yml
    ```

2. **los datos**: Los datos se dividen en crudos (`raw_data`) y procesados (`processed`). Los notebooks proporcionan scripts para procesar y analizar estos datos:

    - `01-inside-airbnb-data.ipynb`: Análisis de datos de Airbnb.
    - `02-scrape-zonaprop-listings.ipynb`: Scraping de listados de Zonaprop.

3. **análisis y ejecución**: Para un análisis detallado y la ejecución del proyecto, revisá `03-load-data-and-run.ipynb` y los notebooks dentro de la carpeta `notebooks`.

## Contribuir

Si estás interesado en contribuir a este proyecto, por favor, revisá `LICENSE` para más detalles sobre cómo hacerlo.

## Contacto

Para cualquier consulta, podés abrir un issue acá en GitHub o mandarme un mail directo a mi casilla (agregar correo electrónico).

¡Espero que este proyecto te sea de utilidad, y cualquier sugerencia o contribución es bienvenida!

