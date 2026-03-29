@extends('layouts.app')

@section('title', 'Carrito - MACUIN')

@section('hero')
<section class="mac-hero">
  <div class="container">
    <h1>Carrito de Compras</h1>
    <p>Revisa tu pedido antes de pagar</p>
  </div>
</section>
@endsection

@section('content')
<div class="row g-3">
  <div class="col-12 col-lg-8">
    <div class="mac-card p-3 p-md-4">
      <div class="fw-bold mb-3">Resumen del Pedido</div>

      @for($i=1; $i<=3; $i++)
      <div class="d-flex gap-3 align-items-center py-3 border-bottom">
        <div class="mac-thumb">IMAGEN<br>PRODUCTO</div>

        <div class="flex-grow-1">
          <div class="fw-bold">Nombre producto</div>
          <div class="text-muted small">Marca</div>
          <div class="fw-bold mt-1">$00.00</div>
        </div>

        <div class="text-center" style="min-width:140px;">
          <div class="small text-muted">Cantidad</div>
          <div class="input-group input-group-sm mt-1 justify-content-center">
            <button class="btn btn-outline-secondary">-</button>
            <input class="form-control text-center" value="1" style="max-width:50px;">
            <button class="btn btn-outline-secondary">+</button>
          </div>
        </div>

        <div class="text-end" style="min-width:120px;">
          <div class="small text-muted">Total</div>
          <div class="fw-bold">$00.00</div>
          <button class="btn btn-sm btn-mac mt-2">Eliminar</button>
        </div>
      </div>
      @endfor
    </div>
  </div>

  <div class="col-12 col-lg-4">
    <div class="mac-card p-3 p-md-4">
      <div class="fw-bold mb-3">Resumen</div>

      <div class="d-flex justify-content-between mb-2">
        <span class="text-muted">Subtotal</span>
        <span class="fw-bold">$00.00</span>
      </div>
      <div class="d-flex justify-content-between mb-2">
        <span class="text-muted">Costo envío</span>
        <span class="fw-bold">$00.00</span>
      </div>
      <hr>
      <div class="d-flex justify-content-between">
        <span class="text-muted">Total (IVA incluido)</span>
        <span class="fw-bold">$00.00</span>
      </div>

      <button class="btn btn-mac w-100 mt-3 py-2">Ir a Pagar</button>
      <div class="text-center mt-2">
        <a href="{{ route('catalog') }}" class="small text-decoration-none">&lt; Seguir comprando</a>
      </div>
    </div>
  </div>
</div>
@endsection
