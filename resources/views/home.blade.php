<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Web Gis</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        #map { height: 500px; }
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        var geojsonData = JSON.parse(@json($geojsonData));
        var colorMapping = JSON.parse(@json($colorMapping));
        var map = L.map('map').setView([-1.269160, 116.825264], 6);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // Fetch FWI data and update the map
        $.ajax({
            url: '{{ route("fwi-data0") }}',
            method: 'GET',
            beforeSend: function(xhr) {
                let token = $('meta[name="csrf-token"]').attr('content');
                xhr.setRequestHeader('X-CSRF-TOKEN', token);
            },
            success: function(response) {
                console.log("AJAX call succeeded:", response);

                if (response.status === 'success') {
                    var colorMapping = response.colorMapping;
                    console.log("Color Mapping:", colorMapping); // Logging color mapping

                    geojsonData.forEach(function(data) {
                        var geojsonLayer = L.geoJSON(data.data, {
                            style: function(feature) {
                                var alt_name = feature.properties.alt_name;

                                if (colorMapping.hasOwnProperty(alt_name)) {
                                    return {
                                        fillColor: colorMapping[alt_name],
                                        weight: 2,
                                        opacity: 1,
                                        color: 'white',
                                        fillOpacity: 0.7
                                    };
                                } else {
                                    return {
                                        fillColor: 'gray',
                                        weight: 2,
                                        opacity: 1,
                                        color: 'white',
                                        fillOpacity: 0.7
                                    };
                                }
                            }
                        }).addTo(map);
                    });
                } else {
                    console.error("Response status not success:", response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX call failed:', xhr.responseText);
                console.error('Status:', status);
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>