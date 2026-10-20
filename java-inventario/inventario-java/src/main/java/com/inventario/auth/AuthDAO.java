package com.inventario.auth;

import com.inventario.ConexionBD;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Acceso a datos para registrar y consultar usuarios.
 */
public class AuthDAO {

    /**
     * Crea la tabla de usuarios si todavía no existe.
     */
    public void inicializarTabla() throws SQLException {
        String sql = """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )
                """;

        try (Connection conexion = ConexionBD.conectar();
             var sentencia = conexion.createStatement()) {
            sentencia.execute(sql);
        }
    }

    /**
     * Registra un usuario con su contraseña previamente cifrada mediante hash.
     */
    public boolean registrar(String usuario, String passwordHash)
            throws SQLException {

        String sql = """
                INSERT INTO usuarios (usuario, password_hash)
                VALUES (?, ?)
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setString(1, usuario);
            sentencia.setString(2, passwordHash);
            sentencia.executeUpdate();
            return true;
        }
    }

    /**
     * Busca el hash de la contraseña asociada a un usuario.
     */
    public String obtenerPasswordHash(String usuario) throws SQLException {
        String sql = """
                SELECT password_hash
                FROM usuarios
                WHERE usuario = ?
                """;

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setString(1, usuario);

            try (ResultSet resultado = sentencia.executeQuery()) {
                if (resultado.next()) {
                    return resultado.getString("password_hash");
                }
            }
        }

        return null;
    }

    /**
     * Comprueba si ya existe un usuario con ese nombre.
     */
    public boolean existeUsuario(String usuario) throws SQLException {
        String sql = "SELECT 1 FROM usuarios WHERE usuario = ? LIMIT 1";

        try (Connection conexion = ConexionBD.conectar();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {

            sentencia.setString(1, usuario);

            try (ResultSet resultado = sentencia.executeQuery()) {
                return resultado.next();
            }
        }
    }
}
