@extends('layouts.app')

@section('title', 'Pedido #' . $pedido['id'] . ' - MACUIN')

@section('content')
@php
    $est = strtoupper($pedido['estatus'] ?? 'PENDIENTE');
    $colorBadge = [
        'PENDIENTE' => 'bg-soft-secondary',
        'SURTIDO'   => 'bg-soft-warning',
        'ENVIADO'   => 'bg-soft-success',
        'RECIBIDO'  => 'bg-soft-info',
        'CANCELADO' => 'bg-soft-secondary',
    ];
    $badge = $colorBadge[$est] ?? 'bg-soft-secondary';
@endphp

<div class="container-fluid pt-3">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Detalle del Pedido #{{ $pedido['id'] }}</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">
                <i class="bi bi-calendar3 me-1"></i>
                {{ \Carbon\Carbon::parse($pedido['fecha_pedido'])->format('d \d\e F \d\e Y, H:i') }}
            </p>
        </div>
        <span class="badge badge-modern {{ $badge }} fs-6">
            @if($est === 'PENDIENTE')
                <i class="bi bi-inbox me-1"></i>Pendiente
            @elseif($est === 'SURTIDO')
                <i class="bi bi-box-seam me-1"></i>Surtido
            @elseif($est === 'ENVIADO')
                <i class="bi bi-truck me-1"></i>Enviado
            @elseif($est === 'RECIBIDO')
                <i class="bi bi-check2-circle me-1"></i>Recibido
            @else
                {{ ucfirst(strtolower($est)) }}
            @endif
        </span>
    </div>

    {{-- Tarjetas de resumen --}}
    <div class="row g-3 mb-4">
        <div class="col-6 col-md-4">
            <div class="content-card p-3 text-center">
                <div class="text-muted small mb-1">Número de pedido</div>
                <div class="fw-bold fs-5" style="color:var(--mac-primary);"># {{ $pedido['id'] }}</div>
            </div>
        </div>
        <div class="col-6 col-md-4">
            <div class="content-card p-3 text-center">
                <div class="text-muted small mb-1">Total del pedido</div>
                <div class="fw-bold fs-4 text-success">${{ number_format($pedido['total'], 2) }}</div>
            </div>
        </div>
        <div class="col-12 col-md-4">
            <div class="content-card p-3 text-center">
                <div class="text-muted small mb-1">Estado actual</div>
                <span class="badge badge-modern {{ $badge }} fs-6">{{ ucfirst(strtolower($est)) }}</span>
            </div>
        </div>
    </div>

    {{-- Tabla de productos del pedido --}}
    <div class="content-card">
        <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-3">
                <div>
                    <h5 class="fw-bold mb-0 text-dark">Productos del Pedido</h5>
                    <p class="text-muted mb-0" style="font-size:.85rem;">
                        {{ count($pedido['detalles']) }} {{ count($pedido['detalles']) === 1 ? 'artículo' : 'artículos' }}
                    </p>
                </div>
            </div>

            <div class="dashboard-table-container">
                <table class="table table-hover table-striped dashboard-table align-middle">
                    <thead>
                        <tr>
                            <th class="ps-4">Producto</th>
                            <th>Marca</th>
                            <th class="text-center">Cantidad</th>
                            <th class="text-end">Precio unitario</th>
                            <th class="text-end pe-4">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($pedido['detalles'] as $det)
                            <tr>
                                <td class="ps-4 fw-bold text-dark">{{ $det['pieza_nombre'] }}</td>
                                <td>
                                    <span class="badge bg-secondary rounded-pill fw-bold">{{ $det['marca'] }}</span>
                                </td>
                                <td class="text-center fw-bold">{{ $det['cantidad'] }}</td>
                                <td class="text-end">${{ number_format($det['precio_unitario'], 2) }}</td>
                                <td class="text-end fw-bold pe-4 text-success">${{ number_format($det['subtotal'], 2) }}</td>
                            </tr>
                        @endforeach
                    </tbody>
                    <tfoot>
                        <tr style="background:#f9fafb;">
                            <td colspan="4" class="text-end fw-bold pe-3" style="padding:1rem;font-size:.95rem;">
                                TOTAL DEL PEDIDO:
                            </td>
                            <td class="text-end fw-bold pe-4 text-success" style="padding:1rem;font-size:1.1rem;">
                                ${{ number_format($pedido['total'], 2) }}
                            </td>
                        </tr>
                    </tfoot>
                </table>
            </div>

            <div class="mt-4 d-flex gap-2">
                <a href="{{ route('orders.index') }}" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left me-1"></i> Volver a mis pedidos
                </a>
                <a href="{{ route('catalog') }}" class="btn btn-mac">
                    <i class="bi bi-grid-fill me-1"></i> Seguir comprando
                </a>
            </div>
        </div>
    </div>
</div>
@endsection
