package com.inventario;

/**
 * Representa un material registrado en el sistema de inventario.
 */
public class Material {

    private int id;
    private String nombre;
    private String categoria;
    private int cantidad;
    private int stockMinimo;

    /**
     * Constructor vacío requerido por Spring Boot y Thymeleaf.
     */
    public Material() {
    }

    /**
     * Constructor para crear materiales sin especificar el identificador.
     */
    public Material(String nombre, String categoria,
                    int cantidad, int stockMinimo) {
        this.nombre = nombre;
        this.categoria = categoria;
        this.cantidad = cantidad;
        this.stockMinimo = stockMinimo;
    }

    /**
     * Constructor para crear materiales con todos sus datos.
     */
    public Material(int id, String nombre, String categoria,
                    int cantidad, int stockMinimo) {
        this.id = id;
        this.nombre = nombre;
        this.categoria = categoria;
        this.cantidad = cantidad;
        this.stockMinimo = stockMinimo;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public int getStockMinimo() {
        return stockMinimo;
    }

    public void setStockMinimo(int stockMinimo) {
        this.stockMinimo = stockMinimo;
    }

    /**
     * Indica si el material necesita reposición.
     */
    public boolean necesitaReposicion() {
        return cantidad <= stockMinimo;
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