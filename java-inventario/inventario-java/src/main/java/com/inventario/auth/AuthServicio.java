package com.inventario.auth;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 * Contiene la lógica de negocio del registro y la autenticación.
 */
public class AuthServicio {

    private final AuthDAO authDAO = new AuthDAO();

    // BCrypt protege las contraseñas sin almacenarlas en texto plano.
    private final BCryptPasswordEncoder codificador =
            new BCryptPasswordEncoder();

    /**
     * Registra un usuario nuevo y protege su contraseña.
     */
    public boolean registrar(String usuario, String contrasena)
            throws Exception {

        if (usuario == null || usuario.isBlank()
                || contrasena == null || contrasena.length() < 8) {
            throw new IllegalArgumentException(
                    "El usuario es obligatorio y la contraseña debe tener "
                    + "al menos 8 caracteres.");
        }

        if (authDAO.existeUsuario(usuario.trim())) {
            return false;
        }

        String hash = codificador.encode(contrasena);
        authDAO.registrar(usuario.trim(), hash);

        return true;
    }

    /**
     * Verifica las credenciales introducidas por el usuario.
     */
    public boolean autenticar(String usuario, String contrasena)
            throws Exception {

        if (usuario == null || contrasena == null) {
            return false;
        }

        String hash = authDAO.obtenerPasswordHash(usuario.trim());

        // Si el usuario no existe, la autenticación falla.
        return hash != null
                && codificador.matches(contrasena, hash);
    }
}
