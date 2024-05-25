<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\File;
use App\Http\Controllers\GeoJSONLoader;
use App\Http\Controllers\PredictionController;
use App\Http\Controllers\FlaskController;
use App\Http\Controllers\FWIDataController;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/


Route::get('/maps', [GeoJSONLoader::class, 'loader'])->name('home');
Route::get('/fwi-data', [GeoJSONLoader::class, 'getFWIData'])->name('fwi-data0');
Route::get('/maps/tes', [FlaskController::class, 'fetchDataFromFlask']);
Route::post('/predict', [PredictionController::class, 'predict']);

Route::get('/test', [FWIDataController::class, 'index'])->name('test');
Route::post('/get-fwi-data', [FWIDataController::class, 'getFWIData'])->name('fwi-data');

// Route::get('/maps', [GeoJSONLoader::class, 'loader']);
