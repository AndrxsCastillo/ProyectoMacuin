<?php

use Illuminate\Support\Facades\Route;

/* HOME → CATÁLOGO */
Route::get('/', fn() => redirect()->route('catalog'));

/* AUTH */
Route::view('/login', 'auth.login')->name('login');
Route::view('/registro', 'auth.register')->name('register');

/* CERRAR SESIÓN → LOGIN */
Route::get('/logout', function () {
    return redirect()->route('login');
})->name('logout');

/* TIENDA */
Route::view('/catalogo', 'shop.catalog')->name('catalog');
Route::view('/carrito', 'shop.cart')->name('cart');

/* PEDIDOS */
Route::view('/mis-pedidos', 'orders.index')->name('orders.index');
Route::view('/mis-pedidos/detalle', 'orders.show')->name('orders.show');
