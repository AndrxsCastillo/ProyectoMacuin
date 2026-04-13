<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class AuthController extends Controller
{
    private string $apiUrl;

    public function __construct()
    {
        $this->apiUrl = env('API_URL', 'http://api_central:8000');
    }

    public function showLogin()
    {
        if (session('usuario_id')) {
            return redirect()->route('catalog');
        }
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $request->validate([
            'email'    => 'required|email',
            'password' => 'required|min:4',
        ], [
            'email.required'    => 'El correo es obligatorio.',
            'email.email'       => 'Ingresa un correo válido.',
            'password.required' => 'La contraseña es obligatoria.',
            'password.min'      => 'La contraseña debe tener al menos 4 caracteres.',
        ]);

        try {
            $response = Http::timeout(8)->asForm()->post("{$this->apiUrl}/cliente/token", [
                'username' => $request->email,
                'password' => $request->password,
            ]);
        } catch (\Exception $e) {
            return back()->withErrors(['general' => 'No se pudo conectar con el servidor. Intenta de nuevo.'])->withInput();
        }

        if ($response->status() === 401) {
            return back()->withErrors(['general' => 'Correo o contraseña incorrectos.'])->withInput();
        }

        if ($response->status() === 403) {
            return back()->withErrors(['general' => $response->json('detail', 'Tu cuenta está desactivada.')])->withInput();
        }

        if (!$response->successful()) {
            return back()->withErrors(['general' => 'Error al iniciar sesión. Intenta de nuevo.'])->withInput();
        }

        $data = $response->json();

        $request->session()->put('usuario_id', $data['usuario_id']);
        $request->session()->put('nombre',     $data['nombre']);
        $request->session()->put('email',      $data['email']);
        $request->session()->put('token',      $data['access_token']);

        return redirect()->route('catalog')->with('success', '¡Bienvenido, ' . $data['nombre'] . '!');
    }

    public function showRegister()
    {
        if (session('usuario_id')) {
            return redirect()->route('catalog');
        }
        return view('auth.register');
    }

    public function register(Request $request)
    {
        $request->validate([
            'nombre'                 => 'required|min:2|max:100',
            'email'                  => 'required|email|max:150',
            'password'               => 'required|min:6|confirmed',
            'password_confirmation'  => 'required',
        ], [
            'nombre.required'                => 'El nombre es obligatorio.',
            'nombre.min'                     => 'El nombre debe tener al menos 2 caracteres.',
            'email.required'                 => 'El correo es obligatorio.',
            'email.email'                    => 'Ingresa un correo válido.',
            'password.required'              => 'La contraseña es obligatoria.',
            'password.min'                   => 'La contraseña debe tener al menos 6 caracteres.',
            'password.confirmed'             => 'Las contraseñas no coinciden.',
            'password_confirmation.required' => 'Confirma tu contraseña.',
        ]);

        try {
            $response = Http::timeout(8)->post("{$this->apiUrl}/cliente/registro", [
                'nombre'   => $request->nombre,
                'email'    => $request->email,
                'password' => $request->password,
            ]);
        } catch (\Exception $e) {
            return back()->withErrors(['general' => 'No se pudo conectar con el servidor. Intenta de nuevo.'])->withInput();
        }

        if ($response->status() === 400) {
            return back()->withErrors(['email' => $response->json('detail', 'Este correo ya está registrado.')])->withInput();
        }

        if (!$response->successful()) {
            return back()->withErrors(['general' => 'Error al crear la cuenta. Intenta de nuevo.'])->withInput();
        }

        return redirect()->route('login')->with('success', '¡Cuenta creada! Ya puedes iniciar sesión.');
    }

    public function logout(Request $request)
    {
        $request->session()->flush();
        return redirect()->route('login')->with('success', 'Sesión cerrada correctamente.');
    }
}
