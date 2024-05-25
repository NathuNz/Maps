<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PredictionController extends Controller
{
    public function predict(Request $request)
    {
        $data = $request->validate([
            'date' => '2024-05-31',
            'province_id' => '11',
        ]);
        
        // Call the Flask API to get predictions
        $response = Http::post('http://127.0.0.1:5000/predict', $data);

        $result = $response->json();
        $prediction = $result['prediction'];
        
        return response()->json(['prediction' => $prediction]);
    }
}