<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class CartController extends Controller
{
    private string $apiUrl;

    public function __construct()
    {
        $this->apiUrl = rtrim(env('API_URL', 'http://api_central:8000'), '/');
    }

    public function show()
    {
        $cart = session('cart', []);
        return view('shop.cart', ['cart' => array_values($cart)]);
    }

    public function add(Request $request)
    {
        $id = (int) $request->input('autoparte_id');

        if (!$id) {
            return back()->withErrors([
                'general' => 'Producto no válido.',
            ]);
        }

        try {
            $res = Http::timeout(8)->get("{$this->apiUrl}/autopartes/{$id}");
        } catch (\Exception $e) {
            return back()->withErrors([
                'general' => 'No se pudo conectar con el servidor.',
            ]);
        }

        if (!$res->successful()) {
            return back()->withErrors([
                'general' => 'Producto no encontrado.',
            ]);
        }

        $p = $res->json();

        if (!($p['activo'] ?? false)) {
            return back()->withErrors([
                'general' => 'Este producto no está disponible.',
            ]);
        }

        $cart = session('cart', []);
        $key = 'item_' . $id;

        if (isset($cart[$key])) {
            $nuevaCantidad = $cart[$key]['cantidad'] + 1;
            $stockDisp = (int) ($p['stock_actual'] ?? 0);

            if ($nuevaCantidad > $stockDisp) {
                return back()->with('warning', "Solo hay {$stockDisp} unidades disponibles de \"{$p['nombre']}\".");
            }

            $cart[$key]['cantidad'] = $nuevaCantidad;
        } else {
            $cart[$key] = [
                'autoparte_id' => $id,
                'nombre' => $p['nombre'],
                'marca' => $p['marca'],
                'descripcion' => $p['descripcion'] ?? '',
                'precio' => (float) $p['precio'],
                'stock_actual' => (int) ($p['stock_actual'] ?? 0),
                'cantidad' => 1,
            ];
        }

        session(['cart' => $cart]);

        return back()->with('success', '"' . $p['nombre'] . '" agregado al carrito.');
    }

    public function update(Request $request)
    {
        $id = (int) $request->input('autoparte_id');
        $cantidad = (int) $request->input('cantidad', 1);
        $key = 'item_' . $id;

        $cart = session('cart', []);

        if (!isset($cart[$key])) {
            return back();
        }

        if ($cantidad <= 0) {
            unset($cart[$key]);
        } else {
            $stock = (int) $cart[$key]['stock_actual'];
            $cart[$key]['cantidad'] = min($cantidad, $stock);
        }

        session(['cart' => $cart]);

        return back();
    }

    public function remove(Request $request)
    {
        $id = (int) $request->input('autoparte_id');
        $key = 'item_' . $id;

        $cart = session('cart', []);
        unset($cart[$key]);

        session(['cart' => $cart]);

        return back()->with('success', 'Producto eliminado del carrito.');
    }

    public function clear(Request $request)
    {
        session()->forget('cart');
        return back();
    }
}