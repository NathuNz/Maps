<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\File;

class GeoJSONLoader extends Controller
{
    public function loader()
    {
        // Define a mapping between prov_id values and colors
        $colorMapping = [
            '51' => '#ff0000', // Red
            '14' => '#00ff00', // Green
            '52' => '#0000ff', // Blue
            // Add more mappings as needed
        ];

        // Initialize an array to store GeoJSON data
        $geojsonData = [];

        // Load GeoJSON file
        $file = public_path('geojson/Full/prov 37.geojson');

        // Check if the file exists
        if (File::exists($file)) {
            // Read the contents of the file
            $contents = File::get($file);

            // Decode the JSON content to an array
            $geojson = json_decode($contents);

            // Check if decoding was successful
            if ($geojson !== null) {
                // Add GeoJSON data to the array
                $geojsonData[] = [
                    'filename' => 'prov 37',
                    'data' => $geojson
                ];
            } else {
                // Log error if decoding failed
                \Log::error("Error decoding GeoJSON file: prov 37.geojson");
            }
        } else {
            // Log error if file does not exist
            \Log::error("GeoJSON file not found: prov 37.geojson");
        }

        // Pass the GeoJSON data and color mapping to the view
        return view('home', [
            'geojsonData' => $geojsonData,
            'colorMapping' => $colorMapping
        ]);
    }
}