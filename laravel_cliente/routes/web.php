<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\ShopController;
use App\Http\Controllers\CartController;
use App\Http\Controllers\OrderController;

/* ── RAÍZ ──────────────────────────────────────────────── */
Route::get('/', fn() => redirect()->route('catalog'));

/* ── AUTENTICACIÓN ─────────────────────────────────────── */
Route::get('/login',    [AuthController::class, 'showLogin'])->name('login');
Route::post('/login',   [AuthController::class, 'login'])->name('login.post');

Route::get('/registro',  [AuthController::class, 'showRegister'])->name('register');
Route::post('/registro', [AuthController::class, 'register'])->name('register.post');

Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

/* ── TIENDA (pública) ──────────────────────────────────── */
Route::get('/catalogo', [ShopController::class, 'catalog'])->name('catalog');

/* ── CARRITO (accesible sin login, checkout requiere login) */
Route::get('/carrito',           [CartController::class,  'show'])->name('cart');
Route::post('/carrito/agregar',  [CartController::class,  'add'])->name('cart.add');
Route::post('/carrito/actualizar',[CartController::class, 'update'])->name('cart.update');
Route::post('/carrito/eliminar', [CartController::class,  'remove'])->name('cart.remove');

/* ── RUTAS QUE REQUIEREN SESIÓN ACTIVA ─────────────────── */
Route::middleware('auth.client')->group(function () {
    Route::post('/carrito/confirmar', [OrderController::class, 'store'])->name('order.store');

    Route::get('/mis-pedidos',            [OrderController::class, 'index'])->name('orders.index');
    Route::get('/mis-pedidos/{id}',       [OrderController::class, 'show'])->name('orders.show');
});
