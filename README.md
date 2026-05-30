# Australia Under Pressure

FIT2179 Data Visualisation 2 project by Weixiong Li.

## Public visualisation

GitHub Pages: https://wlii0223-ui.github.io/FIT2179-assignment-2/

## Sketch

Sketch PDF: https://wlii0223-ui.github.io/FIT2179-assignment-2/sketch.pdf

## Topic

This single-page Vega-Lite data story examines Australian natural disasters through historical disaster records, DRFA recovery activations, state and local government area patterns, and AIHW human impact measures.

## Data sources

- NEMA DRFA Activation History by LGA: https://data.gov.au/data/dataset/drfa-activation-history-by-lga
- AIDR/AEMKH Disaster Events with Category Impact and Location: https://data.gov.au/data/dataset/disaster-events-with-category-impact-and-location
- AIHW Forces of Nature: https://www.aihw.gov.au/reports/injury/forces-of-nature

## Repository structure

- `index.html` - single-page visualisation.
- `styles.css` - typography, layout and visual styling.
- `js/main.js` - Vega-Lite embedding and responsive chart sizing.
- `visualisations/` - human-readable Vega-Lite JSON specifications.
- `processed_data/` - cleaned and reduced CSV files used by the charts.
- `geo/` - simplified map data.
- `data_sources/` - source/reference data files.
- `scripts/` - data processing scripts.
- `sketch.pdf` - sketch document submitted with the project.

## Data note

DRFA activations show where formal recovery assistance was activated. They do not represent every natural disaster event in Australia. Historical disaster records and AIHW health measures were cleaned and aggregated for comparison.

## AI acknowledgement

Generative AI was used to support project planning, code debugging, layout refinement, annotation wording and metadata checks. The final design decisions, data interpretation and submitted visualisation remain the author's responsibility.
