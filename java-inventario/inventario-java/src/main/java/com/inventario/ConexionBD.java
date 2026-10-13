package com.inventario;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class ConexionBD {

    private static final String URL = "jdbc:sqlite:inventario.db";

    public static Connection conectar() throws SQLException {
        return DriverManager.getConnection(URL);
    }

    public static void inicializarBaseDatos() throws SQLException {
        String sql = """
                CREATE TABLE IF NOT EXISTS materiales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    cantidad INTEGER NOT NULL DEFAULT 0,
                    stock_minimo INTEGER NOT NULL DEFAULT 0
                )
                """;

        try (Connection conexion = conectar();
             Statement sentencia = conexion.createStatement()) {

            sentencia.execute(sql);
        }
    }
}
