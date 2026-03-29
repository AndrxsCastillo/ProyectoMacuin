<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>@yield('title', 'MACUIN')</title>
  @vite(['resources/css/app.css', 'resources/js/app.js'])
  <style>
    :root{
      --mac-purple: #1b0b4f;
      --mac-orange: #f39a1f;
      --mac-bg: #f3f4f6;
    }
    body{ background: var(--mac-bg); }

    .mac-topbar{
      background: #fff;
      border-bottom: 1px solid rgba(0,0,0,.06);
    }
    .mac-brand{
      display:flex; align-items:center; gap:.6rem; font-weight:700; letter-spacing:.3px;
      color:#111827; text-decoration:none;
    }
    .mac-brand__dot{
      width:10px; height:10px; border-radius:999px; background: var(--mac-orange);
      display:inline-block;
    }

    .mac-hero{
      background: var(--mac-purple);
      color:#fff;
      padding: 28px 0;
    }
    .mac-hero h1{ font-size: 1.35rem; margin:0; font-weight:700; }
    .mac-hero p{ margin:.25rem 0 0; opacity:.85; font-size:.95rem; }

    .mac-card{
      background:#fff;
      border: 1px solid rgba(0,0,0,.06);
      border-radius: 14px;
      box-shadow: 0 10px 25px rgba(17,24,39,.06);
    }

    .btn-mac{
      background: var(--mac-orange);
      border-color: var(--mac-orange);
      color:#fff;
      font-weight:600;
    }
    .btn-mac:hover{ filter: brightness(.96); color:#fff; }

    .form-control, .form-select{
      border-radius: 10px;
      padding: .7rem .9rem;
    }

    .mac-badge{
      padding: .35rem .65rem;
      border-radius: 999px;
      font-weight:600;
      font-size:.85rem;
      display:inline-block;
      color:#fff;
    }
    .b-green{ background:#22c55e; }
    .b-blue{ background:#3b82f6; }
    .b-yellow{ background:#f59e0b; }
    .b-red{ background:#ef4444; }

    .mac-thumb{
      width: 74px; height: 74px; border-radius: 12px;
      border:1px solid rgba(0,0,0,.1);
      background: #f9fafb;
      display:flex; align-items:center; justify-content:center;
      font-size:.75rem; color:#6b7280;
    }

    /* PERFIL */
    .mac-profile{
      position: relative;
    }

    .mac-profile summary{
      list-style: none;
    }

    .mac-profile summary::-webkit-details-marker{
      display:none;
    }

    .mac-profile-btn{
      background: var(--mac-orange);
      border: 1px solid var(--mac-orange);
      color:#fff;
      font-weight:600;
      border-radius: .25rem;
      padding: .25rem .5rem;
      font-size: .875rem;
      line-height: 1.5;
      cursor: pointer;
      user-select: none;
      display: inline-flex;
      align-items: center;
      gap: .4rem;
    }

    .mac-profile-btn:hover{
      filter: brightness(.96);
    }

    .mac-profile-menu{
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      min-width: 180px;
      background: #fff;
      border: 1px solid rgba(0,0,0,.08);
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(17,24,39,.10);
      padding: .4rem 0;
      z-index: 1000;
    }

    .mac-profile-menu a{
      display:block;
      padding: .6rem .9rem;
      text-decoration:none;
      color:#111827;
      font-size:.95rem;
    }

    .mac-profile-menu a:hover{
      background:#f3f4f6;
    }
  </style>
</head>
<body>

<nav class="mac-topbar">
  <div class="container py-3 d-flex align-items-center justify-content-between">
    <a class="mac-brand" href="{{ route('catalog') }}">
      <span class="mac-brand__dot"></span>
      <span>MACUIN</span>
    </a>

    <div class="d-flex align-items-center gap-2">
      <a class="btn btn-outline-secondary btn-sm" href="{{ route('catalog') }}">Catálogo</a>
      <a class="btn btn-outline-secondary btn-sm" href="{{ route('orders.index') }}">Mis pedidos</a>
      <a class="btn btn-outline-secondary btn-sm" href="{{ route('cart') }}">🛒</a>

      <details class="mac-profile">
        <summary class="mac-profile-btn">
          Perfil
          <span>▾</span>
        </summary>
        <div class="mac-profile-menu">
          <a href="{{ route('logout') }}">Cerrar sesión</a>
        </div>
      </details>
    </div>
  </div>
</nav>

@yield('hero')

<main class="container py-4">
  @yield('content')
</main>

</body>
</html>
