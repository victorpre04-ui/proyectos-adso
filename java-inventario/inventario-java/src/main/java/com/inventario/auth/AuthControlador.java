package com.inventario.auth;

import java.sql.SQLException;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Expone los endpoints REST para registro e inicio de sesión.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthControlador {

    private final AuthDAO authDAO = new AuthDAO();
    private final AuthServicio authServicio = new AuthServicio();

    /**
     * Inicializa la tabla de usuarios al crear el controlador.
     */
    public AuthControlador() throws SQLException {
        authDAO.inicializarTabla();
    }

    /**
     * Recibe el usuario y la contraseña para registrar una cuenta.
     */
    @PostMapping("/registro")
    public ResponseEntity<Map<String, String>> registrar(
            @RequestBody Credenciales datos) {

        try {
            boolean creado = authServicio.registrar(
                    datos.usuario(), datos.contrasena());

            if (!creado) {
                return ResponseEntity.status(HttpStatus.CONFLICT)
                        .body(Map.of("mensaje",
                                "El usuario ya está registrado."));
            }

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(Map.of("mensaje",
                            "Usuario registrado correctamente."));

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of("mensaje", e.getMessage()));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("mensaje",
                            "No fue posible registrar el usuario."));
        }
    }

    /**
     * Valida las credenciales y devuelve el resultado de autenticación.
     */
    @PostMapping("/login")
    public ResponseEntity<Map<String, String>> iniciarSesion(
            @RequestBody Credenciales datos) {

        try {
            boolean autenticado = authServicio.autenticar(
                    datos.usuario(), datos.contrasena());

            if (autenticado) {
                return ResponseEntity.ok(
                        Map.of("mensaje",
                                "Autenticación satisfactoria."));
            }

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("mensaje",
                            "Error en la autenticación."));

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("mensaje",
                            "No fue posible procesar la solicitud."));
        }
    }

    /**
     * Representa los datos JSON recibidos en las solicitudes.
     */
    public record Credenciales(String usuario, String contrasena) {
    }
}
