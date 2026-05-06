# Data Visualisation 2 HD Plan: Australian Natural Disasters

## Working Title

**Australia Under Pressure: Where Natural Disasters Hit, Who Is Exposed, and How Recovery Burdens Repeat**

## Core Story

Natural disasters in Australia are not evenly distributed. Floods dominate recent recovery activations, bushfires and storms create distinct regional patterns, and the human impact is shaped by age, sex, remoteness and place. The visualisation should guide a general Australian audience from a national overview to local repeated exposure and then to human consequences.

## HD Strategy

- Use official Australian data sources and cite them clearly.
- Use Vega-Lite for all maps and charts.
- Include at least 10 visualisation idioms, with several custom-built or composed views.
- Build a presentation-style scroll page, not an expert dashboard.
- Use concise narrative annotations and visible takeaways for each section.
- Keep downloadable data small by pre-aggregating CSV files for the web page.
- Use a polished editorial / emergency atlas visual style.

## Confirmed Data Sources

### 1. NEMA DRFA Activation History by LGA

- Source: National Emergency Management Agency via data.gov.au
- Page: https://data.gov.au/data/dataset/drfa-activation-history-by-lga
- Local file: `data_sources/drfa_activation_history_by_location_2026_january_30.csv`
- Rows inspected: 5,993
- Coverage: 2006 to 2026
- Useful fields:
  - `Location_Name`
  - `Location_Type`
  - `Location_code`
  - `STATE`
  - `event_name`
  - `highest_drfa_category_group`
  - `hazard_type`
  - `disaster_start_date`
- Strong chart uses:
  - Recent disaster recovery activations by year
  - Hazard type ranking
  - State comparison
  - Repeatedly activated LGAs
  - Category A/B vs C/D support

### 2. AEMKH / AIDR Historical Disaster Events

- Source: Attorney-General's Department / Australian Emergency Management Knowledge Hub via data.gov.au
- Page: https://data.gov.au/data/dataset/disaster-events-with-category-impact-and-location
- Local file: `data_sources/aemkh_disaster_events.csv`
- Rows inspected: 673
- Coverage: historical events up to 2014, with many records dating back to the 1800s
- Useful fields:
  - `title`
  - `description`
  - `startDate`
  - `endDate`
  - `lat`
  - `lon`
  - `Deaths`
  - `Injuries`
  - `Evacuated`
  - `Homeless`
  - `Insured Cost`
  - `Home(s) destroyed`
  - `Building(s) destroyed`
  - `regions`
- Strong chart uses:
  - Historical disaster point map
  - Fatality and injury impact chart
  - Major historical event callouts
  - Disaster type timeline

### 3. AIHW Forces of Nature Injuries

- Source: Australian Institute of Health and Welfare
- Page: https://www.aihw.gov.au/reports/injury/forces-of-nature
- Last updated: 25 Nov 2025
- Useful facts confirmed:
  - 815 hospitalisations in 2023-24
  - 68 deaths in 2022-23
  - Males accounted for 552 hospitalisations and 41 deaths
  - People aged 65+ had high injury burden
  - Northern Territory, Queensland and South Australia had the highest hospitalisation rates
  - Summer accounts for about 40% of injuries
- Strong chart uses:
  - Human impact section
  - Age/sex comparison
  - State or remoteness comparison
  - Key statistic callout

## Proposed Page Structure

### Section 1: National Footprint

Purpose: Give the reader immediate spatial context.

Charts:
1. Symbol map of historical disaster events, using `lat` and `lon`.
2. Bar chart of disaster event categories from historical titles.
3. Annotated callouts for major events with high deaths or losses.

### Section 2: The Modern Recovery Burden

Purpose: Show what recent official recovery activations reveal.

Charts:
4. Line chart of DRFA activations by year from 2006 to 2026.
5. Stacked area chart of DRFA activations by hazard type.
6. Ranked bar chart of top hazard types.
7. State comparison chart of activations.

### Section 3: Repeated Exposure

Purpose: Show that some communities are hit again and again.

Charts:
8. Top 15 LGAs by DRFA activation count.
9. Heatmap: state by hazard type.
10. Small multiples or faceted charts for Flood, Bushfire, Storm and Cyclone.

### Section 4: Human Consequences

Purpose: Connect the geography and recovery burden to people.

Charts:
11. AIHW injury callout panel with hospitalisations/deaths.
12. Bar or dot plot by sex / age / state, depending on available extractable AIHW table detail.
13. Historical event impact bubble chart: deaths vs injuries, size by homes/buildings destroyed.

## Recommended Interactions

- Hazard type dropdown for map or time chart.
- Year range slider for DRFA activations.
- Tooltip on every chart with plain-language labels.
- Optional coordinated brushing between time chart and hazard chart.

Avoid heavy interaction that makes the page feel like an expert analysis tool.

## Visual Direction

Use an editorial emergency atlas aesthetic:

- Background: warm off-white or very dark charcoal, but not generic blue dashboard.
- Data colours:
  - Flood: deep blue
  - Bushfire: ember orange/red
  - Storm: violet/steel
  - Cyclone: teal
  - Heat/environmental: ochre
- Base maps should be low contrast so data stands forward.
- Typography should feel like a data journalism feature: strong headline, readable body text, compact labels.
- Use annotations as part of the story, not decorative text.

## Sketch Plan

The sketch must be hand-drawn on paper.

Include:
- Title and subtitle.
- Four labelled sections.
- Map occupying the first visual anchor.
- At least 10 chart boxes with labels.
- Short narrative text blocks beside charts.
- Legends, filters and tooltip notes.
- Data source / author / date area at the bottom.

Do not sketch only empty rectangles. Add enough chart detail to show idiom variety.

## Immediate Next Steps

1. Clean and pre-aggregate the two downloaded CSV files. Done.
2. Create a compact `processed_data` folder for Vega-Lite-ready files. Done.
3. Build two prototype charts first. Done:
   - DRFA activations by year.
   - Historical disaster point map.
4. Use those prototypes to refine the hand sketch. Current step.
   - See `sketch_blueprint.md`.
5. Build the final HTML/CSS/Vega-Lite page.
