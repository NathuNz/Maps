<?php
namespace App\Http\Controllers;

use GuzzleHttp\Client;
use Illuminate\Http\Request;

class FlaskController extends Controller
{
    public function fetchDataFromFlask()
    {
        // Make HTTP request to Flask API
        $client = new Client();
        $response = $client->request('GET', 'http://localhost:5000/api/data');
        $data = json_decode($response->getBody(), true);
        // Process $data as needed
        return view('tes', ['message' => $data['message']]);
    }
}