@extends('layouts.app')

@section('title', 'Catálogo - MACUIN')

@section('content')
<style>
    .btn-agregar {
        background-color: var(--mac-accent);
        color: #111827;
        border: 1px solid var(--mac-accent);
        border-radius: .4rem;
        font-weight: 700;
        font-size: .85rem;
        padding: .4rem .8rem;
        transition: all .2s;
    }
    .btn-agregar:hover {
        background-color: #d97706;
        color: #111827;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(245,158,11,.3);
    }
    .filter-btn.active {
        background-color: var(--mac-primary) !important;
        color: #fff !important;
        border-color: var(--mac-primary) !important;
    }
</style>

<div class="container-fluid pt-3">

    {{-- Cabecera de página --}}
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Catálogo de Autopartes</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">
                {{ $total }} {{ $total === 1 ? 'producto encontrado' : 'productos encontrados' }}
            </p>
        </div>
        {{-- Buscador --}}
        <form method="GET" action="{{ route('catalog') }}" class="d-flex gap-2">
            <input
                class="form-control"
                style="min-width:240px;border-radius:.5rem;"
                name="busqueda"
                placeholder="Buscar nombre, marca, categoría…"
                value="{{ $busqueda }}"
            >
            <button class="btn btn-mac px-3" type="submit">
                <i class="bi bi-search"></i>
            </button>
            @if($busqueda || $categoriaId)
                <a href="{{ route('catalog') }}" class="btn btn-outline-secondary px-3">
                    <i class="bi bi-x-lg"></i>
                </a>
            @endif
        </form>
    </div>

    <div class="row g-3">

        {{-- ── Sidebar filtros ─────────────────────────────────── --}}
        <div class="col-12 col-lg-2">
            <div class="content-card p-3">
                <div class="fw-bold mb-3" style="font-size:.9rem;text-transform:uppercase;letter-spacing:.05em;color:var(--mac-primary);">
                    <i class="bi bi-funnel-fill me-1"></i> Categorías
                </div>
                <div class="d-flex flex-column gap-1">
                    <a href="{{ route('catalog', array_filter(['busqueda' => $busqueda])) }}"
                       class="btn btn-sm text-start rounded-3 filter-btn {{ !$categoriaId ? 'active' : 'btn-outline-secondary' }}">
                        Todas
                    </a>
                    @foreach($categorias as $cat)
                        <a href="{{ route('catalog', array_filter(['busqueda' => $busqueda, 'categoria' => $cat['id']])) }}"
                           class="btn btn-sm text-start rounded-3 filter-btn {{ $categoriaId == $cat['id'] ? 'active' : 'btn-outline-secondary' }}">
                            {{ $cat['nombre'] }}
                        </a>
                    @endforeach
                </div>
            </div>
        </div>

        {{-- ── Tabla de productos ───────────────────────────────── --}}
        <div class="col-12 col-lg-10">
            <div class="content-card">
                <div class="card-body p-4">

                    @if(count($productos) === 0)
                        <div class="text-center py-5">
                            <i class="bi bi-search text-muted" style="font-size:2.5rem;"></i><br>
                            <span class="text-muted fw-bold mt-2 d-block">Sin resultados</span>
                            <small class="text-muted">No encontramos autopartes que coincidan con tu búsqueda.</small>
                            <div class="mt-3">
                                <a href="{{ route('catalog') }}" class="btn btn-mac px-4">Ver todo el catálogo</a>
                            </div>
                        </div>
                    @else
                        <div class="dashboard-table-container">
                            <table class="table table-hover table-striped dashboard-table align-middle">
                                <thead>
                                    <tr>
                                        <th class="ps-4" style="width:5%;">#</th>
                                        <th style="width:30%;">Nombre / Descripción</th>
                                        <th style="width:14%;">Categoría</th>
                                        <th style="width:12%;">Marca</th>
                                        <th class="text-center" style="width:10%;">Stock</th>
                                        <th style="width:11%;">Precio</th>
                                        <th class="text-center" style="width:18%;">Agregar al carrito</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @foreach($productos as $p)
                                        @php $disponible = ($p['stock_actual'] ?? 0) > 0; @endphp
                                        <tr>
                                            <td class="ps-4 fw-bold text-muted">{{ $loop->iteration + ($page - 1) * 9 }}</td>
                                            <td>
                                                <strong class="text-dark">{{ $p['nombre'] }}</strong><br>
                                                @if(!empty($p['descripcion']))
                                                    <span class="text-muted" style="font-size:.85rem;">
                                                        {{ Str::limit($p['descripcion'], 55) }}
                                                    </span>
                                                @endif
                                            </td>
                                            <td>
                                                <span class="badge bg-secondary rounded-pill fw-bold">
                                                    {{ $p['categoria_nombre'] ?? 'Sin categoría' }}
                                                </span>
                                            </td>
                                            <td>
                                                <span class="badge bg-secondary rounded-pill fw-bold">{{ $p['marca'] }}</span>
                                            </td>
                                            <td class="text-center">
                                                @if($disponible)
                                                    @if(($p['stock_actual'] ?? 0) <= ($p['stock_minimo'] ?? 5))
                                                        <div class="d-flex align-items-center justify-content-center text-warning fw-bold" title="Pocas unidades">
                                                            <i class="bi bi-exclamation-triangle-fill me-1"></i> {{ $p['stock_actual'] }}
                                                        </div>
                                                    @else
                                                        <span class="fw-bold text-dark">{{ $p['stock_actual'] }}</span>
                                                    @endif
                                                @else
                                                    <span class="badge bg-soft-secondary badge-modern">Agotado</span>
                                                @endif
                                            </td>
                                            <td class="text-success fw-bold">${{ number_format($p['precio'], 2) }}</td>
                                            <td class="text-center">
                                                @if($disponible)
                                                    <form method="POST" action="{{ route('cart.add') }}">
                                                        @csrf
                                                        <input type="hidden" name="autoparte_id" value="{{ $p['id'] }}">
                                                        <button class="btn btn-agregar" type="submit">
                                                            <i class="bi bi-cart-plus me-1"></i> Agregar
                                                        </button>
                                                    </form>
                                                @else
                                                    <button class="btn btn-sm btn-outline-secondary" disabled>Agotado</button>
                                                @endif
                                            </td>
                                        </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>

                        {{-- Paginación --}}
                        @if($pages > 1)
                            <div class="d-flex justify-content-center mt-4">
                                <nav>
                                    <ul class="pagination mb-0">
                                        <li class="page-item {{ $page <= 1 ? 'disabled' : '' }}">
                                            <a class="page-link" href="{{ route('catalog', array_filter(['busqueda' => $busqueda, 'categoria' => $categoriaId, 'page' => $page - 1])) }}">
                                                ‹ Anterior
                                            </a>
                                        </li>
                                        @for($i = 1; $i <= $pages; $i++)
                                            <li class="page-item {{ $i === $page ? 'active' : '' }}">
                                                <a class="page-link" href="{{ route('catalog', array_filter(['busqueda' => $busqueda, 'categoria' => $categoriaId, 'page' => $i])) }}">
                                                    {{ $i }}
                                                </a>
                                            </li>
                                        @endfor
                                        <li class="page-item {{ $page >= $pages ? 'disabled' : '' }}">
                                            <a class="page-link" href="{{ route('catalog', array_filter(['busqueda' => $busqueda, 'categoria' => $categoriaId, 'page' => $page + 1])) }}">
                                                Siguiente ›
                                            </a>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        @endif
                    @endif

                </div>
            </div>
        </div>

    </div>
</div>
@endsection
