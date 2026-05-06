const hazardScale = {
  domain: [
    "Flood / Rainfall",
    "Bushfire",
    "Storm",
    "Cyclone / Tropical Low",
    "Other"
  ],
  range: ["#246a8d", "#c74728", "#6c5f9f", "#1f8c88", "#8b7a62"]
};

const historicalScale = {
  domain: [
    "Flood",
    "Bushfire",
    "Severe Storm",
    "Cyclone",
    "Environmental",
    "Hail",
    "Earthquake",
    "Landslide",
    "Tornado"
  ],
  range: ["#246a8d", "#c74728", "#6c5f9f", "#1f8c88", "#b9852b", "#87913b", "#7a604c", "#8b7a62", "#5a788a"]
};

const drfaYearlySpec = {
  $schema: "https://vega.github.io/schema/vega-lite/v5.json",
  width: "container",
  height: 330,
  data: { url: "../processed_data/drfa_yearly.csv" },
  layer: [
    {
      mark: { type: "area", color: "#d9b27c", opacity: 0.3, line: false },
      encoding: {
        x: { field: "year", type: "ordinal", title: null, axis: { labelAngle: 0 } },
        y: { field: "activations", type: "quantitative", title: "DRFA activations" }
      }
    },
    {
      mark: { type: "line", color: "#9d351f", strokeWidth: 3 },
      encoding: {
        x: { field: "year", type: "ordinal", title: null },
        y: { field: "activations", type: "quantitative" }
      }
    },
    {
      transform: [{ filter: "datum.year == 2022 || datum.year == 2025" }],
      mark: { type: "point", filled: true, size: 90, color: "#1f2422" },
      encoding: {
        x: { field: "year", type: "ordinal" },
        y: { field: "activations", type: "quantitative" },
        tooltip: [
          { field: "year", type: "ordinal", title: "Year" },
          { field: "activations", type: "quantitative", title: "Activations" }
        ]
      }
    }
  ],
  config: {
    background: null,
    axis: { labelFont: "Verdana", titleFont: "Verdana", gridColor: "#e4ded3", domain: false },
    view: { stroke: null }
  }
};

const historicalMapSpec = {
  $schema: "https://vega.github.io/schema/vega-lite/v5.json",
  width: "container",
  height: 510,
  projection: { type: "mercator", center: [134, -27], scale: 640 },
  layer: [
    {
      data: {
        url: "https://cdn.jsdelivr.net/npm/vega-datasets@2/data/world-110m.json",
        format: { type: "topojson", feature: "countries" }
      },
      mark: { type: "geoshape", fill: "#ded7c9", stroke: "#fbf8f1", strokeWidth: 0.5 }
    },
    {
      data: { url: "../processed_data/historical_events_clean.csv" },
      mark: { type: "circle", opacity: 0.72, stroke: "#1f2422", strokeWidth: 0.35 },
      encoding: {
        longitude: { field: "lon", type: "quantitative" },
        latitude: { field: "lat", type: "quantitative" },
        color: {
          field: "category",
          type: "nominal",
          scale: historicalScale,
          legend: { title: "Disaster type", orient: "bottom", columns: 3 }
        },
        size: {
          field: "impact_score",
          type: "quantitative",
          scale: { range: [18, 900] },
          legend: null
        },
        tooltip: [
          { field: "title", type: "nominal", title: "Event" },
          { field: "year", type: "ordinal", title: "Year" },
          { field: "category", type: "nominal", title: "Type" },
          { field: "deaths", type: "quantitative", title: "Deaths", format: "," },
          { field: "injuries", type: "quantitative", title: "Injuries", format: "," },
          { field: "regions", type: "nominal", title: "Regions" }
        ]
      }
    }
  ],
  config: {
    background: null,
    legend: { labelFont: "Verdana", titleFont: "Verdana" },
    view: { stroke: null }
  }
};

vegaEmbed("#drfa_yearly", drfaYearlySpec, { actions: false });
vegaEmbed("#historical_map", historicalMapSpec, { actions: false });
