package com.inventario;

import java.sql.Connection;
import java.sql.SQLException;

public class PruebaConexion {

    public static void main(String[] args) {
        try {
            ConexionBD.inicializarBaseDatos();

            try (Connection conexion = ConexionBD.conectar()) {
                if (conexion != null && !conexion.isClosed()) {
                    System.out.println("Conexion JDBC exitosa.");
                    System.out.println("Base de datos SQLite inicializada correctamente.");
                }
            }

        } catch (SQLException e) {
            System.err.println("Error al conectar con SQLite: " + e.getMessage());
            e.printStackTrace();
        }
    }
}