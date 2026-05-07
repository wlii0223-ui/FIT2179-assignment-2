const charts = [
  ["#national_map", "visualisations/01_national_map.vg.json"],
  ["#historical_categories", "visualisations/02_historical_categories.vg.json"],
  ["#historical_top_impact", "visualisations/03_historical_top_impact.vg.json"],
  ["#drfa_yearly", "visualisations/04_drfa_yearly.vg.json"],
  ["#drfa_hazard_counts", "visualisations/05_drfa_hazard_counts.vg.json"],
  ["#drfa_year_hazard", "visualisations/06_drfa_year_hazard.vg.json"],
  ["#drfa_state_counts", "visualisations/07_drfa_state_counts.vg.json"],
  ["#drfa_state_hazard", "visualisations/08_drfa_state_hazard.vg.json"],
  ["#drfa_hazard_small_multiples", "visualisations/09_drfa_hazard_small_multiples.vg.json"],
  ["#drfa_top_lgas", "visualisations/10_drfa_top_lgas.vg.json"],
  ["#drfa_category_counts", "visualisations/11_drfa_category_counts.vg.json"],
  ["#aihw_summary", "visualisations/12_aihw_summary.vg.json"],
  ["#historical_impact_bubble", "visualisations/13_historical_impact_bubble.vg.json"]
];

const ASSET_VERSION = "20260507g";

function versionedUrl(url) {
  if (/^https?:\/\//.test(url)) {
    return url;
  }

  return `${url}${url.includes("?") ? "&" : "?"}v=${ASSET_VERSION}`;
}

function mergeConfig(spec) {
  const base = {
    axis: {
      labelFont: "Trebuchet MS",
      titleFont: "Trebuchet MS",
      labelFontSize: 16,
      titleFontSize: 17,
      labelColor: "#18211d",
      titleColor: "#18211d",
      labelPadding: 8,
      titlePadding: 12,
      gridColor: "#ded6c8",
      tickColor: "#bdb3a3",
      domain: false
    },
    legend: {
      labelFont: "Trebuchet MS",
      titleFont: "Trebuchet MS",
      labelFontSize: 16,
      titleFontSize: 17,
      labelColor: "#18211d",
      titleColor: "#18211d",
      labelLimit: 240,
      symbolSize: 145,
      padding: 12
    },
    title: {
      font: "Georgia",
      fontSize: 27,
      color: "#07100c",
      subtitleFont: "Trebuchet MS",
      subtitleFontSize: 17,
      subtitleColor: "#18211d",
      subtitlePadding: 9,
      offset: 10,
      anchor: "start"
    },
    header: {
      labelFont: "Georgia",
      labelFontSize: 23,
      labelColor: "#07100c",
      labelPadding: 14
    },
    view: {
      stroke: null
    }
  };

  spec.config = {
    ...(spec.config || {}),
    axis: { ...((spec.config && spec.config.axis) || {}), ...base.axis },
    legend: { ...((spec.config && spec.config.legend) || {}), ...base.legend },
    title: { ...((spec.config && spec.config.title) || {}), ...base.title },
    header: { ...((spec.config && spec.config.header) || {}), ...base.header },
    view: { ...((spec.config && spec.config.view) || {}), ...base.view }
  };
}

function rewriteSpec(spec, target) {
  const containerWidth = target.clientWidth;
  const isWide = target.classList.contains("wide-chart");
  const id = target.id;
  const reserves = {
    national_map: 190,
    historical_categories: 170,
    historical_top_impact: 360,
    drfa_yearly: 150,
    drfa_hazard_counts: 210,
    drfa_year_hazard: 190,
    drfa_state_counts: 210,
    drfa_state_hazard: 230,
    drfa_top_lgas: 265,
    drfa_category_counts: 120,
    aihw_summary: 220,
    historical_impact_bubble: 260
  };
  const reserved = reserves[id] || (isWide ? 190 : 180);
  const fixedWidth = Math.max(260, containerWidth - reserved);

  mergeConfig(spec);

  // Vega-Lite's width is the plotting area, not the whole rendered SVG.
  // Leave room for y-axis labels, legends, titles and internal padding so the
  // final SVG stays inside its card.
  function visit(value) {
    if (Array.isArray(value)) {
      value.forEach(visit);
      return;
    }

    if (!value || typeof value !== "object") {
      return;
    }

    if (value.width === "container") {
      value.width = fixedWidth;
    }

    if (typeof value.url === "string" && value.url.startsWith("../processed_data/")) {
      value.url = value.url.replace("../processed_data/", "processed_data/");
    }

    Object.values(value).forEach(visit);
  }

  visit(spec);
  return spec;
}

async function embedChart(selector, specUrl) {
  const target = document.querySelector(selector);
  if (!target) return;

  const response = await fetch(versionedUrl(specUrl), { cache: "no-store" });
  const spec = await response.json();
  const patchedSpec = rewriteSpec(spec, target);

  return vegaEmbed(selector, patchedSpec, { actions: false, renderer: "svg" });
}

for (const [selector, spec] of charts) {
  embedChart(selector, spec).catch((error) => {
    const target = document.querySelector(selector);
    if (target) {
      target.textContent = `Unable to load ${spec}`;
    }
    console.error(error);
  });
}
