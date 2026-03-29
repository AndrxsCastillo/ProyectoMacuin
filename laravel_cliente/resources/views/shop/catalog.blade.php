@extends('layouts.app')

@section('title', 'Catálogo - MACUIN')

@section('hero')
<section class="mac-hero">
  <div class="container d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3">
    <div>
      <h1>Encuentra tus Autopartes</h1>
      <p>Dale un vistazo a nuestro catálogo</p>
    </div>

    <div class="d-flex flex-column flex-md-row gap-2 align-items-stretch align-items-md-center">
      <div class="bg-white rounded-4 p-2 d-flex gap-2" style="min-width: 320px;">
        <input class="form-control border-0" placeholder="Buscar nombre, marca, categoría">
        <button class="btn btn-mac px-4">Buscar</button>
      </div>

      <div class="dropdown">
        <button class="btn btn-light border rounded-4 px-4 h-100" type="button" data-bs-toggle="dropdown" aria-expanded="false">

        </button>
        <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 rounded-4">
          <li>
            <a class="dropdown-item" href="{{ route('login') }}">Cerrar sesión</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>
@endsection

@section('content')
<div class="row g-3">
  <div class="col-12 col-lg-3">
    <div class="mac-card p-3">
      <div class="fw-bold mb-2">Categorías</div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="c1"><label class="form-check-label" for="c1">Frenos</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="c2"><label class="form-check-label" for="c2">Motor</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="c3"><label class="form-check-label" for="c3">Suspensión</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="c4"><label class="form-check-label" for="c4">Electricidad</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="c5"><label class="form-check-label" for="c5">Carrocería</label></div>

      <hr>

      <div class="fw-bold mb-2">Marca</div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m1"><label class="form-check-label" for="m1">Bosch</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m2"><label class="form-check-label" for="m2">Brembo</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m3"><label class="form-check-label" for="m3">NGK</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m4"><label class="form-check-label" for="m4">Monroe</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m5"><label class="form-check-label" for="m5">LTH</label></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" id="m6"><label class="form-check-label" for="m6">Denso</label></div>
    </div>
  </div>

  <div class="col-12 col-lg-9">
    <div class="row g-3">

      <!-- Producto 1 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-success-subtle">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-success">Disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Filtro de Aceite</h6>
            <p class="mb-1 text-muted">Marca: <strong>Bosch</strong></p>
            <p class="small text-muted">Sistema de filtrado para motor</p>
            <div class="fw-bold">$250.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-mac btn-sm px-3">Añadir</button>
          </div>
        </div>
      </div>

      <!-- Producto 2 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-success-subtle">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-success">Disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Pastillas de Freno</h6>
            <p class="mb-1 text-muted">Marca: <strong>Brembo</strong></p>
            <p class="small text-muted">Sistema de frenado delantero</p>
            <div class="fw-bold">$780.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-mac btn-sm px-3">Añadir</button>
          </div>
        </div>
      </div>

      <!-- Producto 3 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-secondary-subtle opacity-75">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-secondary">No disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Bujía</h6>
            <p class="mb-1 text-muted">Marca: <strong>NGK</strong></p>
            <p class="small text-muted">Encendido para motor gasolina</p>
            <div class="fw-bold">$120.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-secondary btn-sm px-3" disabled>No disponible</button>
          </div>
        </div>
      </div>

      <!-- Producto 4 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-success-subtle">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-success">Disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Amortiguador</h6>
            <p class="mb-1 text-muted">Marca: <strong>Monroe</strong></p>
            <p class="small text-muted">Suspensión delantera</p>
            <div class="fw-bold">$1,250.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-mac btn-sm px-3">Añadir</button>
          </div>
        </div>
      </div>

      <!-- Producto 5 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-secondary-subtle opacity-75">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-secondary">No disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Batería Automotriz</h6>
            <p class="mb-1 text-muted">Marca: <strong>LTH</strong></p>
            <p class="small text-muted">12V para automóvil</p>
            <div class="fw-bold">$2,100.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-secondary btn-sm px-3" disabled>No disponible</button>
          </div>
        </div>
      </div>

      <!-- Producto 6 -->
      <div class="col-12 col-md-6 col-xl-4">
        <div class="mac-card p-3 h-100 border border-success-subtle">
          <div class="rounded-4 border d-flex align-items-center justify-content-center position-relative" style="height:140px;background:#f9fafb;">
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill text-bg-success">Disponible</span>
            IMAGEN
          </div>

          <div class="mt-3">
            <h6 class="fw-bold">Radiador</h6>
            <p class="mb-1 text-muted">Marca: <strong>Denso</strong></p>
            <p class="small text-muted">Sistema de enfriamiento</p>
            <div class="fw-bold">$1,950.00</div>
          </div>

          <div class="mt-3 d-flex justify-content-end">
            <button class="btn btn-mac btn-sm px-3">Añadir</button>
          </div>
        </div>
      </div>

    </div>

    <div class="d-flex justify-content-center mt-4">
      <nav>
        <ul class="pagination">
          <li class="page-item"><a class="page-link" href="#">« Anterior</a></li>
          <li class="page-item active"><a class="page-link" href="#">1</a></li>
          <li class="page-item"><a class="page-link" href="#">2</a></li>
          <li class="page-item"><a class="page-link" href="#">3</a></li>
          <li class="page-item"><a class="page-link" href="#">Siguiente »</a></li>
        </ul>
      </nav>
    </div>
  </div>
</div>
@endsection
