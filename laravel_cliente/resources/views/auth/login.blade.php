@extends('layouts.app')

@section('title', 'Iniciar Sesión - MACUIN')

@section('content')
<div class="container-fluid pt-3">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Iniciar Sesión</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">Accede para gestionar tu carrito y tus pedidos</p>
        </div>
    </div>

    <div class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-5">
            <div class="content-card p-4 p-md-5">

                <div class="text-center mb-4">
                    <div class="fw-bold fs-5" style="color:var(--mac-primary);">MACUIN</div>
                    <h3 class="h4 mt-2 mb-1 fw-bold">Bienvenido de vuelta</h3>
                    <small class="text-muted">Introduce los datos de tu cuenta de cliente</small>
                </div>

                @if($errors->has('general'))
                    <div class="alert alert-danger border-0 rounded-3 mb-3">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ $errors->first('general') }}
                    </div>
                @endif

                <form method="POST" action="{{ route('login.post') }}" novalidate>
                    @csrf

                    <div class="mb-3">
                        <label class="form-label fw-semibold text-dark">Correo electrónico</label>
                        <input
                            class="form-control form-control-lg @error('email') is-invalid @enderror"
                            type="email"
                            name="email"
                            placeholder="tu@correo.com"
                            value="{{ old('email') }}"
                            autofocus
                            autocomplete="email"
                        >
                        @error('email')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-semibold text-dark">Contraseña</label>
                        <input
                            class="form-control form-control-lg @error('password') is-invalid @enderror"
                            type="password"
                            name="password"
                            placeholder="••••••••"
                            autocomplete="current-password"
                        >
                        @error('password')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <button type="submit" class="btn btn-mac w-100 py-2 fs-5 shadow-sm">
                        <i class="bi bi-box-arrow-in-right me-2"></i>Iniciar Sesión
                    </button>

                    <div class="text-center mt-4">
                        <small>¿No tienes cuenta? <a href="{{ route('register') }}" style="color:var(--mac-primary);font-weight:600;">Crear cuenta</a></small>
                    </div>
                </form>

            </div>
        </div>
    </div>
</div>
@endsection
