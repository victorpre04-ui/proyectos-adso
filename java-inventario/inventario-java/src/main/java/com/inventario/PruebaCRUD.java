package com.inventario;

import java.sql.SQLException;

public class PruebaCRUD {

    public static void main(String[] args) {
        MaterialDAO materialDAO = new MaterialDAO();
        int idMaterial = -1;

        try {
            // 1. Inicializar la base de datos.
            ConexionBD.inicializarBaseDatos();

            // 2. INSERTAR un material de prueba.
            Material material = new Material(
                    "MATERIAL PRUEBA CRUD",
                    "PRUEBAS",
                    35,
                    5
            );

            boolean insertado = materialDAO.insertar(material);
            System.out.println("Material insertado: " + insertado);

            // 3. Localizar el registro que acabamos de insertar.
            for (Material m : materialDAO.listar()) {
                if ("MATERIAL PRUEBA CRUD".equals(m.getNombre())
                        && "PRUEBAS".equals(m.getCategoria())) {
                    idMaterial = m.getId();
                }
            }

            if (idMaterial == -1) {
                System.out.println("No se encontró el material de prueba.");
                return;
            }

            // 4. CONSULTAR el material por su identificador.
            Material encontrado = materialDAO.buscarPorId(idMaterial);
            System.out.println("Material consultado: " + encontrado);

            // 5. ACTUALIZAR la cantidad.
            encontrado.setCantidad(34);
            boolean actualizado = materialDAO.actualizar(encontrado);
            System.out.println("Material actualizado: " + actualizado);

            // 6. ELIMINAR exclusivamente el registro de prueba.
            boolean eliminado = materialDAO.eliminar(idMaterial);
            System.out.println("Material eliminado: " + eliminado);

        } catch (SQLException e) {
            System.err.println("Error durante la prueba CRUD: " + e.getMessage());
            e.printStackTrace();
        }
    }
}