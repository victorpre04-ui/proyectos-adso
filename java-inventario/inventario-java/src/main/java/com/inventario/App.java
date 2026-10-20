package com.inventario;

import java.sql.SQLException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.inventario.auth.AuthDAO;

/**
 * Punto de entrada de la aplicación web de inventario.
 */
@SpringBootApplication
public class App {

    public static void main(String[] args) throws SQLException {

        // Inicializa la base de datos antes de iniciar la aplicación.
        ConexionBD.inicializarBaseDatos();

        // Inicializa la tabla de usuarios para la autenticación.
        new AuthDAO().inicializarTabla();

        // Inicia el servidor web de Spring Boot.
        SpringApplication.run(App.class, args);
    }
}
