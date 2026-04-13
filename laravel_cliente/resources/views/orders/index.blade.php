@extends('layouts.app')

@section('title', 'Mis Pedidos - MACUIN')

@section('content')
<div class="container-fluid pt-3">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Mis Pedidos</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">Consulta el estado y detalle de tus compras</p>
        </div>
        <a href="{{ route('catalog') }}" class="btn btn-mac shadow-sm">
            <i class="bi bi-grid-fill me-2"></i>Seguir comprando
        </a>
    </div>

    @php
        $colorBadge = [
            'PENDIENTE' => 'bg-soft-secondary',
            'SURTIDO'   => 'bg-soft-warning',
            'ENVIADO'   => 'bg-soft-success',
            'RECIBIDO'  => 'bg-soft-info',
            'CANCELADO' => 'bg-soft-secondary',
        ];
    @endphp

    <div class="content-card">
        <div class="card-body p-4">
            @if(count($pedidos) === 0)
                <div class="text-center py-5">
                    <i class="bi bi-receipt text-muted" style="font-size:2.5rem;"></i><br>
                    <span class="text-muted fw-bold mt-2 d-block">Aún no tienes pedidos</span>
                    <small class="text-muted">Explora nuestro catálogo y realiza tu primera compra.</small>
                    <div class="mt-3">
                        <a href="{{ route('catalog') }}" class="btn btn-mac px-5">
                            <i class="bi bi-grid-fill me-1"></i> Ir al catálogo
                        </a>
                    </div>
                </div>
            @else
                <div class="dashboard-table-container">
                    <table class="table table-hover table-striped dashboard-table align-middle">
                        <thead>
                            <tr>
                                <th class="ps-4" style="width:14%;"># Pedido</th>
                                <th style="width:22%;">Fecha</th>
                                <th style="width:16%;">Total</th>
                                <th style="width:20%;">Estado</th>
                                <th class="text-end pe-4" style="width:28%;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($pedidos as $pedido)
                                @php
                                    $est   = strtoupper($pedido['estatus'] ?? 'PENDIENTE');
                                    $badge = $colorBadge[$est] ?? 'bg-soft-secondary';
                                    $fecha = \Carbon\Carbon::parse($pedido['fecha_pedido'])->format('d/m/Y H:i');
                                @endphp
                                <tr>
                                    <td class="ps-4 fw-bold text-muted">ORD-{{ $pedido['id'] }}</td>
                                    <td>
                                        <i class="bi bi-calendar3 text-muted me-2" style="font-size:.8rem;"></i>
                                        <span class="fw-medium text-dark">{{ $fecha }}</span>
                                    </td>
                                    <td class="text-success fw-bold">${{ number_format($pedido['total'], 2) }}</td>
                                    <td>
                                        @if($est === 'PENDIENTE')
                                            <span class="badge badge-modern bg-soft-secondary">
                                                <i class="bi bi-inbox me-1"></i>Pendiente
                                            </span>
                                        @elseif($est === 'SURTIDO')
                                            <span class="badge badge-modern bg-soft-warning">
                                                <i class="bi bi-box-seam me-1"></i>Surtido
                                            </span>
                                        @elseif($est === 'ENVIADO')
                                            <span class="badge badge-modern bg-soft-success">
                                                <i class="bi bi-truck me-1"></i>Enviado
                                            </span>
                                        @elseif($est === 'RECIBIDO')
                                            <span class="badge badge-modern bg-soft-info">
                                                <i class="bi bi-check2-circle me-1"></i>Recibido
                                            </span>
                                        @else
                                            <span class="badge badge-modern bg-soft-secondary">{{ ucfirst(strtolower($est)) }}</span>
                                        @endif
                                    </td>
                                    <td class="text-end pe-4">
                                        <a href="{{ route('orders.show', $pedido['id']) }}"
                                           class="btn btn-mac btn-sm">
                                            <i class="bi bi-eye me-1"></i> Ver detalle
                                        </a>
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @endif
        </div>
    </div>
</div>
@endsection
