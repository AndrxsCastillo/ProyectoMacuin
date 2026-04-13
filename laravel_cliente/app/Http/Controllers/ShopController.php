<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ShopController extends Controller
{
    private string $apiUrl;

    public function __construct()
    {
        $this->apiUrl = env('API_URL', 'http://api_central:8000');
    }

    public function catalog(Request $request)
    {
        // Cargar categorías para los filtros
        $categorias = [];
        try {
            $catRes = Http::timeout(8)->get("{$this->apiUrl}/categorias/");
            if ($catRes->successful()) {
                $categorias = $catRes->json();
            }
        } catch (\Exception $e) {
            // Continuar sin categorías si la API no responde
        }

        // Cargar todos los productos
        $productos = [];
        try {
            $prodRes = Http::timeout(8)->get("{$this->apiUrl}/autopartes/", ['limit' => 200]);
            if ($prodRes->successful()) {
                $productos = $prodRes->json();
            }
        } catch (\Exception $e) {
            // Continuar sin productos
        }

        // ── Filtros del cliente ──────────────────────────────────────
        $busqueda   = trim($request->input('busqueda', ''));
        $categoriaId = $request->input('categoria');

        if ($busqueda !== '') {
            $needle = mb_strtolower($busqueda);
            $productos = array_filter($productos, function ($p) use ($needle) {
                return str_contains(mb_strtolower($p['nombre']      ?? ''), $needle)
                    || str_contains(mb_strtolower($p['marca']       ?? ''), $needle)
                    || str_contains(mb_strtolower($p['descripcion'] ?? ''), $needle)
                    || str_contains(mb_strtolower($p['categoria_nombre'] ?? ''), $needle);
            });
        }

        if ($categoriaId) {
            $productos = array_filter($productos, fn($p) => ($p['categoria_id'] ?? null) == $categoriaId);
        }

        // Solo mostrar activos con stock
        $productos = array_values(array_filter($productos, fn($p) => $p['activo'] ?? false));

        // ── Paginación simple ────────────────────────────────────────
        $perPage  = 9;
        $page     = max(1, (int) $request->input('page', 1));
        $total    = count($productos);
        $pages    = max(1, (int) ceil($total / $perPage));
        $page     = min($page, $pages);
        $slice    = array_slice($productos, ($page - 1) * $perPage, $perPage);

        return view('shop.catalog', [
            'productos'   => $slice,
            'categorias'  => $categorias,
            'busqueda'    => $busqueda,
            'categoriaId' => $categoriaId,
            'page'        => $page,
            'pages'       => $pages,
            'total'       => $total,
        ]);
    }
}
