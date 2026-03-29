@extends('layouts.app')

@section('title', 'Crear cuenta - MACUIN')

@section('hero')
<section class="mac-hero">
  <div class="container">
    <h1>Crea tu Cuenta</h1>
    <p>O <a class="text-white text-decoration-underline" href="{{ route('login') }}">Inicia Sesión</a> para explorar todas nuestras funciones</p>
  </div>
</section>
@endsection

@section('content')
<div class="row justify-content-center">
  <div class="col-12 col-md-7 col-lg-5">
    <div class="mac-card p-4 p-md-5">
      <div class="text-center mb-4">
        <div class="fw-bold">MACUIN</div>
        <h2 class="h4 mt-2 mb-0">Crear Cuenta</h2>
      </div>

      <form>
        <div class="mb-3">
          <input class="form-control" placeholder="Nombre Completo">
        </div>
        <div class="mb-3">
          <input class="form-control" placeholder="Correo electrónico">
        </div>
        <div class="mb-3">
          <input class="form-control" type="password" placeholder="Contraseña">
        </div>
        <div class="mb-3">
          <input class="form-control" type="password" placeholder="Confirmar contraseña">
        </div>

        <button type="button" class="btn btn-mac w-100 py-2">Registrarse</button>

        <div class="text-center mt-3">
          <small>¿Ya tienes cuenta? <a href="{{ route('login') }}">Inicia Sesión</a></small>
        </div>
      </form>
    </div>
  </div>
</div>
@endsection