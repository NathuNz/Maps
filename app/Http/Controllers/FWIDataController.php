<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\File;

class FWIDataController extends Controller
{
    public function index()
    {
        $geojsonData = [];
        $file = public_path('geojson/Full/alldata.geojson');

        if (File::exists($file)) {
            $contents = File::get($file);
            $geojson = json_decode($contents, true); // Decode as associative array
            if ($geojson !== null) {
                $geojsonData = $geojson; // Directly assign the decoded JSON data
            } else {
                \Log::error("Error decoding GeoJSON file: alldata.geojson");
            }
        } else {
            \Log::error("GeoJSON file not found: alldata.geojson");
        }

        return view('test', [
            'geojsonData' => json_encode($geojsonData),
            'colorMapping' => json_encode([]) // Initial empty color mapping
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

        $date = $request->input('date');

        $response = Http::post('http://127.0.0.1:5000/api/fwi-data-all', [
            'date' => $date,
        ]);

        if ($response->successful()) {
            $fwiData = $response->json();
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
        } else {
            return response()->json([
                'status' => 'error',
                'message' => 'No data found or an error occurred.'
            ]);
        }
    }
}
