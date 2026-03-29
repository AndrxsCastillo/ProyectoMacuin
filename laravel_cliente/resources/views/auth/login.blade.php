@extends('layouts.app')

@section('title', 'Iniciar sesión - MACUIN')

@section('hero')
<section class="mac-hero">
    <div class="container">
        <h1>Inicia Sesión</h1>
        <p>Accede para revisar tu carrito y tus pedidos</p>
    </div>
</section>
@endsection

@section('content')
<div class="row justify-content-center">
    <div class="col-12 col-md-8 col-lg-5">
        <div class="mac-card p-4 p-md-5">
            <div class="text-center mb-4">
                <div class="fw-bold fs-5">MACUIN</div>
                <h2 class="h2 mt-2 mb-1">Iniciar Sesión</h2>
                <small class="text-muted d-block">Introduce los detalles de tu cuenta</small>
            </div>

            <form>
                <div class="mb-3">
                    <input
                        class="form-control form-control-lg"
                        type="email"
                        placeholder="Correo electrónico"
                    >
                    <small class="text-muted">Usa el correo con el que te registraste</small>
                </div>

                <div class="mb-2">
                    <input
                        class="form-control form-control-lg"
                        type="password"
                        placeholder="Contraseña"
                    >
                </div>

                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <div class="form-check m-0">
                        <input class="form-check-input" type="checkbox" id="remember">
                        <label class="form-check-label" for="remember">Recordarme</label>
                    </div>

                    <a href="#" class="small text-decoration-none">¿Olvidaste tu contraseña?</a>
                </div>

                <a href="{{ route('catalog') }}" class="btn btn-mac w-100 py-2 fs-5">
                    Iniciar Sesión
                </a>

                <div class="text-center mt-4">
                    <small>¿No tienes cuenta? <a href="{{ route('register') }}">Crear cuenta</a></small>
                </div>
            </form>
        </div>
    </div>
</div>
@endsection
