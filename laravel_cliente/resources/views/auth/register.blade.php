@extends('layouts.app')

@section('title', 'Crear Cuenta - MACUIN')

@section('content')
<div class="container-fluid pt-3">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h2 class="fw-bold mb-0 text-dark">Crear Cuenta</h2>
            <p class="text-muted mb-0" style="font-size:.9rem;">
                ¿Ya tienes cuenta?
                <a href="{{ route('login') }}" style="color:var(--mac-primary);font-weight:600;">Inicia sesión aquí</a>
            </p>
        </div>
    </div>

    <div class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-5">
            <div class="content-card p-4 p-md-5">

                <div class="text-center mb-4">
                    <div class="fw-bold fs-5" style="color:var(--mac-primary);">MACUIN</div>
                    <h3 class="h4 mt-2 mb-0 fw-bold">Nueva cuenta de cliente</h3>
                </div>

                @if($errors->has('general'))
                    <div class="alert alert-danger border-0 rounded-3 mb-3">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ $errors->first('general') }}
                    </div>
                @endif

                <form method="POST" action="{{ route('register.post') }}" novalidate>
                    @csrf

                    <div class="mb-3">
                        <label class="form-label fw-semibold text-dark">Nombre completo</label>
                        <input
                            class="form-control @error('nombre') is-invalid @enderror"
                            type="text"
                            name="nombre"
                            placeholder="Tu nombre completo"
                            value="{{ old('nombre') }}"
                            autofocus
                            autocomplete="name"
                        >
                        @error('nombre')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold text-dark">Correo electrónico</label>
                        <input
                            class="form-control @error('email') is-invalid @enderror"
                            type="email"
                            name="email"
                            placeholder="tu@correo.com"
                            value="{{ old('email') }}"
                            autocomplete="email"
                        >
                        @error('email')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold text-dark">Contraseña <small class="text-muted">(mínimo 6 caracteres)</small></label>
                        <input
                            class="form-control @error('password') is-invalid @enderror"
                            type="password"
                            name="password"
                            placeholder="••••••••"
                            autocomplete="new-password"
                        >
                        @error('password')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-semibold text-dark">Confirmar contraseña</label>
                        <input
                            class="form-control @error('password_confirmation') is-invalid @enderror"
                            type="password"
                            name="password_confirmation"
                            placeholder="••••••••"
                            autocomplete="new-password"
                        >
                        @error('password_confirmation')
                            <div class="invalid-feedback">{{ $message }}</div>
                        @enderror
                    </div>

                    <button type="submit" class="btn btn-mac w-100 py-2 shadow-sm">
                        <i class="bi bi-person-check-fill me-2"></i>Crear mi cuenta
                    </button>

                    <div class="text-center mt-3">
                        <small>¿Ya tienes cuenta? <a href="{{ route('login') }}" style="color:var(--mac-primary);font-weight:600;">Iniciar Sesión</a></small>
                    </div>
                </form>

            </div>
        </div>
    </div>
</div>
@endsection
