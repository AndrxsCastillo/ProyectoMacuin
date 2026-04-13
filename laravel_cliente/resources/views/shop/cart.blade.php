@extends('layouts.app')

@section('title', 'Carrito - MACUIN')

@section('content')
@php
    $subtotal = array_sum(array_map(fn($i) => $i['precio'] * $i['cantidad'], $cart));
    $total    = $subtotal;
@endphp

<div class="container-fluid pt-3">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Carrito de Compras</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">Revisa tu pedido antes de confirmarlo</p>
        </div>
        <a href="{{ route('catalog') }}" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left me-1"></i> Seguir comprando
        </a>
    </div>

    @if(count($cart) === 0)
        <div class="content-card p-5 text-center">
            <i class="bi bi-cart3 text-muted" style="font-size:3rem;"></i><br>
            <span class="text-muted fw-bold mt-2 d-block">Tu carrito está vacío</span>
            <small class="text-muted">Explora nuestro catálogo y agrega los productos que necesitas.</small>
            <div class="mt-3">
                <a href="{{ route('catalog') }}" class="btn btn-mac px-5">
                    <i class="bi bi-grid-fill me-1"></i> Ver catálogo
                </a>
            </div>
        </div>

    @else
        <div class="row g-3">

            {{-- ── Tabla de productos ───────────────────────────── --}}
            <div class="col-12 col-lg-8">
                <div class="content-card">
                    <div class="card-body p-4">
                        <div class="fw-bold mb-3">
                            {{ count($cart) }} {{ count($cart) === 1 ? 'producto' : 'productos' }} en tu carrito
                        </div>

                        <div class="dashboard-table-container">
                            <table class="table table-hover dashboard-table align-middle">
                                <thead>
                                    <tr>
                                        <th class="ps-4">Producto</th>
                                        <th>Marca</th>
                                        <th class="text-center">Cantidad</th>
                                        <th class="text-end">Precio</th>
                                        <th class="text-end">Subtotal</th>
                                        <th class="text-center">Quitar</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @foreach($cart as $item)
                                        <tr>
                                            <td class="ps-4">
                                                <div class="d-flex align-items-center gap-3">
                                                    <div class="mac-thumb">
                                                        <i class="bi bi-gear-fill text-muted"></i>
                                                    </div>
                                                    <div>
                                                        <div class="fw-bold text-dark">{{ $item['nombre'] }}</div>
                                                        @if(!empty($item['descripcion']))
                                                            <small class="text-muted">{{ Str::limit($item['descripcion'], 40) }}</small>
                                                        @endif
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                <span class="badge bg-secondary rounded-pill fw-bold">{{ $item['marca'] }}</span>
                                            </td>
                                            <td class="text-center">
                                                <form method="POST" action="{{ route('cart.update') }}"
                                                      class="d-flex gap-1 justify-content-center align-items-center">
                                                    @csrf
                                                    <input type="hidden" name="autoparte_id" value="{{ $item['autoparte_id'] }}">
                                                    <button type="submit" name="cantidad" value="{{ $item['cantidad'] - 1 }}"
                                                            class="btn btn-outline-secondary btn-sm"
                                                            style="width:28px;height:28px;padding:0;line-height:1;"
                                                            {{ $item['cantidad'] <= 1 ? 'disabled' : '' }}>−</button>
                                                    <span class="fw-bold mx-2" style="min-width:20px;text-align:center;">
                                                        {{ $item['cantidad'] }}
                                                    </span>
                                                    <button type="submit" name="cantidad" value="{{ $item['cantidad'] + 1 }}"
                                                            class="btn btn-outline-secondary btn-sm"
                                                            style="width:28px;height:28px;padding:0;line-height:1;"
                                                            {{ $item['cantidad'] >= $item['stock_actual'] ? 'disabled' : '' }}>+</button>
                                                </form>
                                            </td>
                                            <td class="text-end fw-bold">${{ number_format($item['precio'], 2) }}</td>
                                            <td class="text-end fw-bold text-success">
                                                ${{ number_format($item['precio'] * $item['cantidad'], 2) }}
                                            </td>
                                            <td class="text-center">
                                                <form method="POST" action="{{ route('cart.remove') }}">
                                                    @csrf
                                                    <input type="hidden" name="autoparte_id" value="{{ $item['autoparte_id'] }}">
                                                    <button type="submit" class="btn btn-sm"
                                                            style="color:#dc2626;background:#fee2e2;border:none;border-radius:.4rem;font-size:.85rem;padding:.4rem .7rem;">
                                                        <i class="bi bi-trash3"></i>
                                                    </button>
                                                </form>
                                            </td>
                                        </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
            </div>

            {{-- ── Resumen del pedido ───────────────────────────── --}}
            <div class="col-12 col-lg-4">
                <div class="content-card p-4">
                    <div class="fw-bold mb-3"
                         style="text-transform:uppercase;letter-spacing:.05em;font-size:.85rem;color:var(--mac-primary);">
                        <i class="bi bi-receipt me-1"></i> Resumen del Pedido
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-muted">Subtotal ({{ count($cart) }} productos)</span>
                        <span class="fw-bold">${{ number_format($subtotal, 2) }}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between mb-4">
                        <span class="fw-bold fs-6">Total</span>
                        <span class="fw-bold fs-5 text-success">${{ number_format($total, 2) }}</span>
                    </div>

                    {{-- Error de la API directamente en el resumen --}}
                    @if($errors->has('general'))
                        <div class="alert alert-danger border-0 rounded-3 mb-3" style="font-size:.9rem;">
                            <i class="bi bi-exclamation-triangle-fill me-2"></i>
                            {{ $errors->first('general') }}
                        </div>
                    @endif

                    @if(session('usuario_id'))
                        <form method="POST" action="{{ route('order.store') }}">
                            @csrf
                            {{-- type="submit" — funciona sin JavaScript --}}
                            <button type="submit" class="btn btn-mac w-100 py-2 fw-bold shadow-sm">
                                <i class="bi bi-check-circle-fill me-2"></i>Confirmar Pedido
                            </button>
                        </form>
                        <p class="text-muted small text-center mt-2 mb-0">
                            <i class="bi bi-shield-check me-1"></i>Pago verificado al entregar
                        </p>
                    @else
                        <a href="{{ route('login') }}" class="btn btn-mac w-100 py-2 fw-bold">
                            <i class="bi bi-box-arrow-in-right me-2"></i>Iniciar sesión para pagar
                        </a>
                        <p class="text-muted small text-center mt-2 mb-0">
                            Tu carrito se guardará al iniciar sesión
                        </p>
                    @endif

                    <div class="text-center mt-3">
                        <a href="{{ route('catalog') }}" class="small text-decoration-none"
                           style="color:var(--mac-primary);">
                            ‹ Seguir comprando
                        </a>
                    </div>
                </div>
            </div>

        </div>
    @endif
</div>
@endsection
