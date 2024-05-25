<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\File;
use GuzzleHttp\Client;
use Illuminate\Http\Request;

class GeoJSONLoader extends Controller
{
    public function loader()
    {
        $file = public_path('geojson/Full/alldata.geojson');
        $geojsonData = [];

        if (File::exists($file)) {
            $contents = File::get($file);
            $geojson = json_decode($contents, true); // Convert to associative array

            if ($geojson !== null) {
                $geojsonData[] = [
                    'filename' => 'alldata',
                    'data' => $geojson
                ];
            } else {
                \Log::error("Error decoding GeoJSON file: alldata.geojson");
            }
        } else {
            \Log::error("GeoJSON file not found: alldata.geojson");
        }

        return view('home', [
            'geojsonData' => json_encode($geojsonData), // Properly encode as JSON
            'colorMapping' => json_encode([]) // Initially empty
        ]);
    }

    public function getFWIData(Request $request)
    {
        $defineColorMapping = [
            'low' => '#ADD8E6',
            'normal' => '#00FF00',
            'high' => '#FFFF00',
            'extreme' => '#FF0000'
        ];

        $client = new Client();
        $response = $client->request('GET', 'http://localhost:5000/api/fwi-data-0');
        $fwiData = json_decode($response->getBody(), true);
        $colorMapping = [];

        foreach ($fwiData as $entry) {
            $alt_name = $entry['name'];
            $fwi = $entry['FWI'];

            if ($fwi < 1) {
                $colorMapping[$alt_name] = $defineColorMapping['low'];
            } elseif ($fwi < 6) {
                $colorMapping[$alt_name] = $defineColorMapping['normal'];
            } elseif ($fwi < 13) {
                $colorMapping[$alt_name] = $defineColorMapping['high'];
            } else {
                $colorMapping[$alt_name] = $defineColorMapping['extreme'];
            }
        }

        return response()->json([
            'status' => 'success',
            'colorMapping' => $colorMapping,
            'data' => $fwiData
        ]);
    }
}
