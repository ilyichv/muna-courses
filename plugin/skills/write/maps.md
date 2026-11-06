# Map cards

The author brings the map. Don't look for, simplify or license map data yourself: if the course has no GeoJSON file for a map card, ask the author for one.

## The map file
`"map": "regions"` means `regions.geojson` in the course folder, next to `course.json`. It's a `FeatureCollection` in longitude/latitude, at most 5 MB:

```json
{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "properties": { "id": "north", "name": "North" },
      "geometry": { "type": "Polygon", "coordinates": [[[9, 45], [12, 45], [12, 47], [9, 47], [9, 45]]] } },
    { "type": "Feature", "properties": { "id": "sea", "quizzable": false },
      "geometry": { "type": "Polygon", "coordinates": [[[12, 42], [14, 42], [14, 44], [12, 44], [12, 42]]] } }
  ]
}
```
- Every feature needs `properties.id`, which cards name in `feature`. If the author's file has other properties (`ISO_A3`, `name`), ask which one to copy into `id`.
- `quizzable: false` draws a shape that's never an answer (seas, neighbours). It defaults to true. Other properties are ignored.

## The card
```json
{ "id": "rome-geo-001", "type": "map", "prompt": "Find the north", "map": "regions", "feature": "north" }
```
The validator checks that the file exists and that `feature` is a quizzable feature in it.

## Credit
If the map comes from someone else's data, the course folder needs an `ATTRIBUTION.md` naming the source, its licence, and what was changed. Remind the author, and ask them for the source and licence rather than guessing.
