<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'MACUIN - Tienda')</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

    <style>
        :root {
            --mac-primary:       #065F46;   /* Verde bosque profundo */
            --mac-primary-hover: #064E3B;
            --mac-accent:        #F59E0B;   /* Ámbar dorado */
            --mac-body-bg:       #f3f4f6;
        }

        body {
            background-color: var(--mac-body-bg);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #111827;
        }

        /* ── Navbar ─────────────────────────────────────────── */
        .mac-navbar {
            background-color: var(--mac-primary);
            padding-top: 1.2rem;
            padding-bottom: 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .navbar-brand {
            font-weight: 800;
            font-size: 1.6rem;
            color: white !important;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: 0.05em;
            text-decoration: none;
        }

        .navbar-brand .brand-dot {
            width: 12px; height: 12px;
            border-radius: 999px;
            background: var(--mac-accent);
            display: inline-block;
            flex-shrink: 0;
        }

        .nav-link {
            color: rgba(255,255,255,.85) !important;
            font-weight: 600;
            font-size: 1.05rem;
            margin-left: .5rem;
            margin-right: .5rem;
            transition: color .2s ease;
        }

        .nav-link:hover, .nav-link.active {
            color: var(--mac-accent) !important;
        }

        /* Badge del carrito en el nav */
        .cart-nav-badge {
            background: var(--mac-accent);
            color: #111;
            font-size: .7rem;
            font-weight: 700;
            border-radius: 999px;
            padding: 1px 6px;
            margin-left: 4px;
            vertical-align: middle;
        }

        /* ── Botón Cerrar Sesión ─────────────────────────────── */
        .btn-logout {
            background-color: var(--mac-accent);
            color: #111827;
            font-weight: 700;
            border-radius: .5rem;
            padding: .5rem 1.2rem;
            transition: all .2s;
            border: none;
            cursor: pointer;
        }

        .btn-logout:hover {
            background-color: #d97706;
            color: #111827;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(245,158,11,.3);
        }

        /* ── Contenido principal ─────────────────────────────── */
        .main-content {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* ── Overrides Bootstrap con colores MACUIN ─────────── */
        .bg-primary { background-color: var(--mac-primary) !important; }
        .text-primary { color: var(--mac-primary) !important; }
        .btn-primary {
            background-color: var(--mac-primary) !important;
            border-color: var(--mac-primary) !important;
        }
        .btn-primary:hover {
            background-color: var(--mac-primary-hover) !important;
            border-color: var(--mac-primary-hover) !important;
        }
        .border-primary { border-color: var(--mac-primary) !important; }

        /* ── Botón acción principal (ámbar) ──────────────────── */
        .btn-mac {
            background-color: var(--mac-accent);
            border-color: var(--mac-accent);
            color: #111827;
            font-weight: 700;
            border-radius: .5rem;
            transition: all .2s;
        }
        .btn-mac:hover {
            background-color: #d97706;
            border-color: #d97706;
            color: #111827;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(245,158,11,.3);
        }
        .btn-mac:disabled { opacity: .6; cursor: not-allowed; }

        /* ── Cards ───────────────────────────────────────────── */
        .content-card {
            background-color: #ffffff;
            border: none;
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,.05), 0 10px 10px -5px rgba(0,0,0,.04);
        }

        /* ── Tablas estilo panel admin ───────────────────────── */
        .dashboard-table-container {
            border-radius: .75rem;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }

        .dashboard-table { margin-bottom: 0; width: 100%; }

        .dashboard-table thead th {
            border: none;
            background-color: var(--mac-primary);
            color: #ffffff;
            text-transform: uppercase;
            font-weight: 800;
            font-size: .8rem;
            letter-spacing: .05em;
            padding: 1rem;
        }

        .dashboard-table tbody tr {
            transition: background-color .2s ease-in-out;
        }

        .dashboard-table tbody tr:hover { background-color: #f9fafb; }

        .dashboard-table tbody td {
            vertical-align: middle;
            padding: 1.25rem 1rem;
            font-size: .95rem;
            border-bottom: 1px solid #f3f4f6;
        }

        /* ── Inputs ──────────────────────────────────────────── */
        .form-control, .form-select {
            border-radius: 10px;
            padding: .7rem .9rem;
        }
        .form-control.is-invalid, .form-select.is-invalid {
            border-color: #ef4444;
        }
        .form-control:focus, .form-select:focus {
            border-color: var(--mac-primary);
            box-shadow: 0 0 0 .2rem rgba(6,95,70,.15);
        }

        /* ── Badges de estado ────────────────────────────────── */
        .mac-badge {
            padding: .35rem .65rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: .85rem;
            display: inline-block;
            color: #fff;
        }
        .b-gray   { background: #6b7280; }
        .b-green  { background: #22c55e; }
        .b-blue   { background: #3b82f6; }
        .b-yellow { background: #f59e0b; color: #111; }
        .b-red    { background: #ef4444; }
        .b-purple { background: #8b5cf6; }

        /* Soft badges para tablas */
        .badge-modern {
            padding: .5rem .8rem;
            font-weight: 700;
            font-size: .8rem;
            border-radius: .5rem;
        }
        .bg-soft-secondary { background-color: #f3f4f6; color: #4b5563; border: 1px solid #d1d5db; }
        .bg-soft-warning   { background-color: #fff7ed; color: #b45309; border: 1px solid #fed7aa; }
        .bg-soft-success   { background-color: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
        .bg-soft-info      { background-color: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }

        /* ── Thumbnail producto ───────────────────────────────── */
        .mac-thumb {
            width: 52px; height: 52px; border-radius: 10px;
            border: 1px solid rgba(0,0,0,.1);
            background: #f9fafb;
            display: flex; align-items: center; justify-content: center;
            font-size: .85rem; color: #6b7280;
            flex-shrink: 0;
        }

        /* ── Alertas flash ───────────────────────────────────── */
        .fade-out {
            opacity: 0;
            transition: opacity .5s ease-out;
        }

        /* ── Modal estilos ───────────────────────────────────── */
        .modal-warning-header {
            background-color: #f8f9fa;
            border-bottom: 2px solid #fef3c7;
            padding: 1rem 1.5rem;
        }
        .modal-warning-icon {
            font-size: 1.5rem;
            color: var(--mac-accent);
            margin-right: .75rem;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg mac-navbar sticky-top">
    <div class="container-fluid px-4">

        <a class="navbar-brand" href="{{ route('catalog') }}">
            <span class="brand-dot"></span>
            MACUIN
        </a>

        <button class="navbar-toggler border-0 shadow-none" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-expanded="false">
            <i class="bi bi-list text-white fs-1"></i>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-4">
                <li class="nav-item">
                    <a class="nav-link" href="{{ route('catalog') }}">
                        <i class="bi bi-grid-fill me-1"></i> Catálogo
                    </a>
                </li>
                @php $cartCount = array_sum(array_column(session('cart', []), 'cantidad')); @endphp
                <li class="nav-item">
                    <a class="nav-link" href="{{ route('cart') }}">
                        <i class="bi bi-cart3 me-1"></i> Carrito
                        @if($cartCount > 0)
                            <span class="cart-nav-badge">{{ $cartCount }}</span>
                        @endif
                    </a>
                </li>
                @if(session('usuario_id'))
                <li class="nav-item">
                    <a class="nav-link" href="{{ route('orders.index') }}">
                        <i class="bi bi-receipt me-1"></i> Mis Pedidos
                    </a>
                </li>
                @endif
            </ul>

            <div class="d-flex align-items-center mt-3 mt-lg-0 gap-2">
                @if(session('usuario_id'))
                    <span class="text-white fw-bold" style="font-size:.95rem;">
                        <i class="bi bi-person-circle me-1 text-white-50"></i>
                        {{ Str::limit(session('nombre'), 18) }}
                    </span>
                    <button type="button" id="btn-trigger-logout" class="btn btn-logout ms-3">
                        <i class="bi bi-box-arrow-right me-1"></i> Cerrar Sesión
                    </button>
                    <form method="POST" action="{{ route('logout') }}" id="form-real-logout" class="d-none">
                        @csrf
                    </form>
                @else
                    <a href="{{ route('login') }}" class="nav-link">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Iniciar Sesión
                    </a>
                    <a href="{{ route('register') }}" class="btn btn-logout">
                        <i class="bi bi-person-plus me-1"></i> Crear cuenta
                    </a>
                @endif
            </div>
        </div>
    </div>
</nav>

<main class="main-content container-fluid px-4">

    {{-- Alertas flash --}}
    @if(session('success') || session('warning'))
        <div id="flash-messages-container" class="mt-1 mb-2">
            @if(session('success'))
                <div class="alert alert-success alert-dismissible fade show shadow-sm border-0 auto-dismiss-alert" role="alert">
                    <i class="bi bi-check-circle-fill me-2"></i>{{ session('success') }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            @endif
            @if(session('warning'))
                <div class="alert alert-warning alert-dismissible fade show shadow-sm border-0 auto-dismiss-alert" role="alert">
                    <i class="bi bi-exclamation-circle-fill me-2"></i>{{ session('warning') }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            @endif
        </div>
    @endif

    @yield('content')
</main>

{{-- Modal de Cerrar Sesión (igual al Flask admin) --}}
<div class="modal fade" id="modalCerrarSesion" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content border-0 shadow-lg">
            <div class="modal-header modal-warning-header d-flex align-items-center">
                <i class="bi bi-box-arrow-right modal-warning-icon"></i>
                <h5 class="modal-title fw-bold text-dark mb-0">Cerrar Sesión</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4 text-center">
                <p class="text-dark fs-6 mb-0">¿Estás seguro que deseas cerrar tu sesión en MACUIN?</p>
            </div>
            <div class="modal-footer bg-light border-top-0 d-flex justify-content-center gap-2">
                <button type="button" class="btn btn-secondary fw-bold px-4" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-mac fw-bold px-4 shadow-sm" id="btnConfirmarLogout">Sí, salir</button>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss de alertas a los 5 segundos
    document.querySelectorAll('.auto-dismiss-alert').forEach(function (alerta) {
        setTimeout(function () {
            alerta.classList.add('fade-out');
            setTimeout(function () {
                const inst = bootstrap.Alert.getOrCreateInstance(alerta);
                if (inst) inst.close();
            }, 500);
        }, 5000);
    });

    // Modal de cerrar sesión
    let modalLogoutUI = null;
    const btnTrigger = document.getElementById('btn-trigger-logout');
    const formLogout = document.getElementById('form-real-logout');
    const btnConfirmar = document.getElementById('btnConfirmarLogout');

    if (btnTrigger) {
        btnTrigger.addEventListener('click', function (e) {
            e.preventDefault();
            if (!modalLogoutUI) {
                modalLogoutUI = new bootstrap.Modal(document.getElementById('modalCerrarSesion'));
            }
            modalLogoutUI.show();
        });
    }

    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', function () {
            if (formLogout) formLogout.submit();
        });
    }
});
</script>
</body>
</html>
