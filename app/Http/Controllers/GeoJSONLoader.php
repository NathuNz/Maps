<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\File;

class GeoJSONLoader extends Controller
{
    public function loader()
    {
        // Initialize an array to store GeoJSON data
        $geojsonData = [];

        // Get all GeoJSON files in the directory
        $files = File::files(public_path('geojson/11x'));

        // Loop through each file
        foreach ($files as $file) {
            // Read the contents of the file
            $contents = File::get($file);
            
            // Decode the JSON content to an array
            $geojson = json_decode($contents);

            // Add GeoJSON data to the array
            $geojsonData[] = $geojson;
        }

        // Pass the GeoJSON data to the view
        return view('home', ['geojsonData' => $geojsonData]);
    }
}
