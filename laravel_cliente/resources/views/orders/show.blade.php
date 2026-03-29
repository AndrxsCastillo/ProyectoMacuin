@extends('layouts.app')

@section('title', 'Detalle de pedido - MACUIN')

@section('hero')
<section class="mac-hero">
  <div class="container">
    <h1>Detalle del Pedido</h1>
    <p>Información del pedido y productos</p>
  </div>
</section>
@endsection

@section('content')
<div class="mac-card p-3 p-md-4">
  <div class="d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 mb-3">
    <div class="fw-bold fs-5">Pedido #1547</div>
    <div class="d-flex gap-2 align-items-center">
      <span class="text-muted">Estado</span>
      <span class="mac-badge b-blue">Enviado</span>
    </div>
  </div>

  <div class="row g-3 mb-3">
    <div class="col-12 col-md-4">
      <div class="p-3 rounded-4 border bg-light">
        <div class="text-muted small">Fecha del Pedido</div>
        <div class="fw-bold">22/01/26</div>
      </div>
    </div>
    <div class="col-12 col-md-4">
      <div class="p-3 rounded-4 border bg-light">
        <div class="text-muted small">Total</div>
        <div class="fw-bold">$00.00</div>
      </div>
    </div>
    <div class="col-12 col-md-4 d-flex align-items-stretch">
      <button class="btn btn-mac w-100">Descargar Comprobante</button>
    </div>
  </div>

  <div class="table-responsive">
    <table class="table align-middle">
      <thead>
        <tr>
          <th>Producto</th>
          <th>Cantidad</th>
          <th>Precio Unitario</th>
          <th>Subtotal</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Nombre</td><td>1</td><td>$00.00</td><td>$00.00</td></tr>
        <tr><td>Nombre</td><td>1</td><td>$00.00</td><td>$00.00</td></tr>
        <tr><td>Nombre</td><td>1</td><td>$00.00</td><td>$00.00</td></tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="3" class="text-end fw-bold">TOTAL:</td>
          <td class="fw-bold">$00.00</td>
        </tr>
      </tfoot>
    </table>
  </div>

  <div class="mt-3">
    <a href="{{ route('orders.index') }}" class="btn btn-outline-secondary">Volver</a>
  </div>
</div>
@endsection