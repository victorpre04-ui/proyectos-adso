package com.inventario;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class MaterialDAO {

    // Registrar un material en la base de datos.
    public boolean insertar(Material material) throws SQLException {
        String sql = """
                INSERT INTO materiales
                (nombre, categoria, cantidad, stock_minimo)
                VALUES (?, ?, ?, ?)
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setString(1, material.getNombre());
            sentencia.setString(2, material.getCategoria());
            sentencia.setInt(3, material.getCantidad());
            sentencia.setInt(4, material.getStockMinimo());

            return sentencia.executeUpdate() > 0;
        }
    }

    // Consultar todos los materiales registrados.
    public List<Material> listar() throws SQLException {
        List<Material> materiales = new ArrayList<>();

        String sql = """
                SELECT id, nombre, categoria, cantidad, stock_minimo
                FROM materiales
                ORDER BY id
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql);
             ResultSet resultado = sentencia.executeQuery()) {

            while (resultado.next()) {
                Material material = new Material(
                        resultado.getInt("id"),
                        resultado.getString("nombre"),
                        resultado.getString("categoria"),
                        resultado.getInt("cantidad"),
                        resultado.getInt("stock_minimo")
                );

                materiales.add(material);
            }
        }

        return materiales;
    }

    // Consultar un material por su identificador.
    public Material buscarPorId(int id) throws SQLException {
        String sql = """
                SELECT id, nombre, categoria, cantidad, stock_minimo
                FROM materiales
                WHERE id = ?
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setInt(1, id);

            try (ResultSet resultado = sentencia.executeQuery()) {
                if (resultado.next()) {
                    return new Material(
                            resultado.getInt("id"),
                            resultado.getString("nombre"),
                            resultado.getString("categoria"),
                            resultado.getInt("cantidad"),
                            resultado.getInt("stock_minimo")
                    );
                }
            }
        }

        return null;
    }

    // Actualizar los datos de un material.
    public boolean actualizar(Material material) throws SQLException {
        String sql = """
                UPDATE materiales
                SET nombre = ?, categoria = ?, cantidad = ?, stock_minimo = ?
                WHERE id = ?
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setString(1, material.getNombre());
            sentencia.setString(2, material.getCategoria());
            sentencia.setInt(3, material.getCantidad());
            sentencia.setInt(4, material.getStockMinimo());
            sentencia.setInt(5, material.getId());

            return sentencia.executeUpdate() > 0;
        }
    }

    // Eliminar un material por su identificador.
    public boolean eliminar(int id) throws SQLException {
        String sql = "DELETE FROM materiales WHERE id = ?";

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setInt(1, id);

            return sentencia.executeUpdate() > 0;
        }
    }
}