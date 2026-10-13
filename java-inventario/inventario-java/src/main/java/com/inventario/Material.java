package com.inventario;

public class Material {

    private int id;
    private String nombre;
    private String categoria;
    private int cantidad;
    private int stockMinimo;

    public Material(int id, String nombre, String categoria,
                    int cantidad, int stockMinimo) {
        this.id = id;
        this.nombre = nombre;
        this.categoria = categoria;
        this.cantidad = cantidad;
        this.stockMinimo = stockMinimo;
    }

    public Material(String nombre, String categoria,
                    int cantidad, int stockMinimo) {
        this(0, nombre, categoria, cantidad, stockMinimo);
    }

    public int getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getCategoria() {
        return categoria;
    }

    public int getCantidad() {
        return cantidad;
    }

    public int getStockMinimo() {
        return stockMinimo;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public void setStockMinimo(int stockMinimo) {
        this.stockMinimo = stockMinimo;
    }

    @Override
    public String toString() {
        return "Material{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", categoria='" + categoria + '\'' +
                ", cantidad=" + cantidad +
                ", stockMinimo=" + stockMinimo +
                '}';
    }
}