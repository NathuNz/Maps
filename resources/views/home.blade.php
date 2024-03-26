<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Web Gis</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>
     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
     integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
     crossorigin=""></script>
     <style>
        #map { height: 500px; }
        </style>
</head>
<body>
    <div id="map"></div>
</body>
<script>
    //memunculkan map leaflet
    var map = L.map('map').setView([-1.269160, 116.825264], 6);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var colorMapping = @json($colorMapping);

@foreach($geojsonData as $geojson)
    var geojsonLayer = L.geoJson(@json($geojson['data'])).addTo(map);
    
    // Check if color mapping exists for the filename
    if (colorMapping.hasOwnProperty(@json($geojson['filename']))) {
        var color = colorMapping[@json($geojson['filename'])];
        // Set color of the GeoJSON layer
        geojsonLayer.setStyle({
            fillColor: color,
            color: color
        });
    }
@endforeach
</script>
</html>