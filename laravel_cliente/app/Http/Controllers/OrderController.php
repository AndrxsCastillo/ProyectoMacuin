<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class OrderController extends Controller
{
    private string $apiUrl;

    public function __construct()
    {
        $this->apiUrl = rtrim(env('API_URL', 'http://api_central:8000'), '/');
    }

    public function index()
    {
        $usuarioId = session('usuario_id');
        $pedidos = [];

        if (!$usuarioId) {
            return redirect()->route('login')
                ->withErrors(['general' => 'Debes iniciar sesión para ver tus pedidos.']);
        }

        try {
            $res = Http::timeout(8)->get("{$this->apiUrl}/cliente/pedidos/", [
                'usuario_id' => $usuarioId,
            ]);

            if ($res->successful()) {
                $pedidos = $res->json();
            }
        } catch (\Exception $e) {
            // Mostrar vista con lista vacía
        }

        return view('orders.index', ['pedidos' => $pedidos]);
    }

    public function show(int $id)
    {
        $usuarioId = session('usuario_id');

        if (!$usuarioId) {
            return redirect()->route('login')
                ->withErrors(['general' => 'Debes iniciar sesión para ver el pedido.']);
        }

        try {
            $res = Http::timeout(8)->get("{$this->apiUrl}/pedidos/{$id}");
        } catch (\Exception $e) {
            return redirect()->route('orders.index')
                ->withErrors(['general' => 'No se pudo cargar el pedido.']);
        }

        if ($res->status() === 404) {
            abort(404, 'Pedido no encontrado.');
        }

        if (!$res->successful()) {
            return redirect()->route('orders.index')
                ->withErrors(['general' => 'Error al cargar el pedido.']);
        }

        $pedido = $res->json();

        // Verificar que el pedido pertenece al usuario en sesión
        try {
            $listRes = Http::timeout(8)->get("{$this->apiUrl}/cliente/pedidos/", [
                'usuario_id' => $usuarioId,
            ]);

            if ($listRes->successful()) {
                $ids = array_column($listRes->json(), 'id');
                if (!in_array($id, $ids)) {
                    abort(403, 'No tienes permiso para ver este pedido.');
                }
            }
        } catch (\Exception $e) {
            // Si falla la verificación, permitir el acceso
        }

        return view('orders.show', ['pedido' => $pedido]);
    }

    public function store(Request $request)
    {
        $cart = session('cart', []);
        $usuarioId = session('usuario_id');

        if (!$usuarioId) {
            return redirect()->route('login')
                ->withErrors(['general' => 'Debes iniciar sesión para confirmar tu compra.']);
        }

        if (empty($cart)) {
            return redirect()->route('cart')
                ->withErrors(['general' => 'Tu carrito está vacío.']);
        }

        $items = [];

        foreach ($cart as $item) {
            $autoparteId = (int) ($item['autoparte_id'] ?? 0);
            $cantidad = (int) ($item['cantidad'] ?? 0);

            if ($autoparteId <= 0 || $cantidad <= 0) {
                continue;
            }

            $items[] = [
                'autoparte_id' => $autoparteId,
                'cantidad' => $cantidad,
            ];
        }

        if (empty($items)) {
            return redirect()->route('cart')
                ->withErrors(['general' => 'No hay productos válidos en el carrito.']);
        }

        try {
            $res = Http::timeout(15)->post("{$this->apiUrl}/cliente/pedidos/", [
                'usuario_id' => (int) $usuarioId,
                'items' => $items,
            ]);
        } catch (\Exception $e) {
            return redirect()->route('cart')
                ->withErrors(['general' => 'No se pudo conectar con el servidor. Intenta de nuevo.']);
        }

        if (!$res->successful()) {
            $detail = $res->json('detail');

            if (is_array($detail)) {
                $detalle = implode(' | ', array_map(
                    fn($e) => $e['msg'] ?? json_encode($e),
                    $detail
                ));
            } else {
                $detalle = $detail ?? 'No se pudo procesar tu pedido. Intenta de nuevo.';
            }

            return redirect()->route('cart')
                ->withErrors(['general' => $detalle]);
        }

        session()->forget('cart');

        $pedido = $res->json();

        return redirect()->route('orders.index')
            ->with('success', '¡Pedido #' . $pedido['id'] . ' realizado con éxito! Total: $' . number_format($pedido['total'], 2));
    }
}