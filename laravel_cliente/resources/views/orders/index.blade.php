@extends('layouts.app')

@section('title', 'Mis pedidos - MACUIN')

@section('hero')
<section class="mac-hero">
  <div class="container">
    <h1>Historial de pedidos</h1>
    <p>Consulta el estado y el detalle de tus compras</p>
  </div>
</section>
@endsection

@section('content')
<div class="mac-card p-3 p-md-4">
  <div class="table-responsive">
    <table class="table align-middle mb-0">
      <thead>
        <tr>
          <th>ID Pedido</th>
          <th>Fecha</th>
          <th>Total</th>
          <th>Estado</th>
          <th class="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>

        <tr>
          <td>1</td><td>15/11/25</td><td>$00.00</td>
          <td><span class="mac-badge b-green">Surtido</span></td>
          <td class="text-end">
            <a class="btn btn-sm btn-outline-secondary" href="{{ route('orders.show') }}">Ver detalles</a>
          </td>
        </tr>

        <tr>
          <td>2</td><td>26/11/25</td><td>$00.00</td>
          <td><span class="mac-badge b-green">Surtido</span></td>
          <td class="text-end">
            <a class="btn btn-sm btn-outline-secondary" href="{{ route('orders.show') }}">Ver detalles</a>
          </td>
        </tr>

        <tr>
          <td>4</td><td>18/12/25</td><td>$00.00</td>
          <td><span class="mac-badge b-blue">Enviado</span></td>
          <td class="text-end">
            <button class="btn btn-sm btn-mac">Descargar comprobante</button>
          </td>
        </tr>

        <tr>
          <td>5</td><td>05/01/26</td><td>$00.00</td>
          <td><span class="mac-badge b-yellow">Recibido</span></td>
          <td class="text-end">
            <button class="btn btn-sm btn-danger">Cancelar</button>
          </td>
        </tr>

      </tbody>
    </table>
  </div>

  <div class="d-flex justify-content-center mt-4">
    <nav>
      <ul class="pagination mb-0">
        <li class="page-item"><a class="page-link" href="#">« Anterior</a></li>
        <li class="page-item active"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">Siguiente »</a></li>
      </ul>
    </nav>
  </div>
</div>
@endsection
