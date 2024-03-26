<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\File;

class GeoJSONLoader extends Controller
{
    public function loader()
    {
        // Define a mapping between filenames and colors
        $colorMapping = [
            'prov 37' => '#ff0000', // Red
            // '11.02' => '#00ff00', // Green

            // Add more mappings as needed
        ];

        // Initialize an array to store GeoJSON data
        $geojsonData = [];

        // Get all GeoJSON files in the directory
        $files = File::files(public_path('geojson/Full'));

        // Loop through each file
        foreach ($files as $file) {
            // Read the filename
            $filename = pathinfo($file->getFilename(), PATHINFO_FILENAME);
            
            // Read the contents of the file
            $contents = File::get($file);
            
            // Decode the JSON content to an array
            $geojson = json_decode($contents);

            // Add GeoJSON data to the array
            $geojsonData[] = [
                'filename' => $filename,
                'data' => $geojson
            ];
        }

        // Pass the GeoJSON data and color mapping to the view
        return view('home', [
            'geojsonData' => $geojsonData,
            'colorMapping' => $colorMapping
        ]);
    }
}