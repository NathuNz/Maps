<!DOCTYPE html>
<html lang="en">
<head>
    <title>FWI Data</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        #map { height: 500px; display: none; }
    </style>
</head>
<body>
    <h1>FWI Data</h1>
    <form id="fwiForm">
        <label for="date">Date:</label>
        <input type="date" id="date" name="date" required>
        <br>
        <button type="submit">Get FWI Data</button>
    </form>

    <div id="results"></div>
    <div id="map"></div>

    <script>
        $(document).ready(function() {
            var map;
            var geojsonLayer;
            var geojsonData = JSON.parse(@json($geojsonData));
            var colorMapping = JSON.parse(@json($colorMapping));

            $('#fwiForm').on('submit', function(event) {
                event.preventDefault();

                let formData = $(this).serialize();

                $.ajax({
                    url: '{{ route("fwi-data") }}',
                    method: 'POST',
                    data: formData,
                    beforeSend: function(xhr) {
                        let token = $('meta[name="csrf-token"]').attr('content');
                        xhr.setRequestHeader('X-CSRF-TOKEN', token);
                    },
                    success: function(response) {
                        $('#results').empty(); // Clear previous results

                        if (response.status === 'success') {
                            let resultHtml = '<h2>Results:</h2><ul>';
                            response.data.forEach(result => {
                                resultHtml += `<li>
                                    Name: ${result.name}<br>
                                    Date: ${result.date}<br>
                                    FFMC: ${result.FFMC}<br>
                                    DMC: ${result.DMC}<br>
                                    DC: ${result.DC}<br>
                                    ISI: ${result.ISI}<br>
                                    BUI: ${result.BUI}<br>
                                    FWI: ${result.FWI}<br>
                                </li>`;
                            });
                            resultHtml += '</ul>';
                            $('#results').html(resultHtml);

                            // Show map div
                            $('#map').show();

                            // Initialize the map only if it is not already initialized
                            if (!map) {
                                map = L.map('map').setView([-1.269160, 116.825264], 6);
                                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                    maxZoom: 19,
                                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                                }).addTo(map);
                            }

                            // Update map with new color mapping
                            if (geojsonLayer) {
                                map.removeLayer(geojsonLayer);
                            }

                            geojsonLayer = L.geoJSON(geojsonData, {
                                style: function (feature) {
                                    var alt_name = feature.properties.alt_name;

                                    if (response.colorMapping.hasOwnProperty(alt_name)) {
                                        return {
                                            fillColor: response.colorMapping[alt_name],
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
                        } else {
                            $('#results').html('<p>' + response.message + '</p>');
                        }
                    },
                    error: function(xhr, status, error) {
                        $('#results').empty(); // Clear previous results
                        $('#results').html('<p>An error occurred</p>');
                    }
                });
            });
        });
    </script>
</body>
</html>