package com.inventario.controlador;

import java.sql.SQLException;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.inventario.Material;
import com.inventario.MaterialDAO;

/**
 * Controlador web para gestionar los materiales del inventario.
 */
@Controller
public class MaterialControlador {

    private final MaterialDAO materialDAO = new MaterialDAO();

    /**
     * Muestra los materiales registrados.
     */
    @GetMapping("/")
    public String listarMateriales(Model modelo) throws SQLException {
        List<Material> materiales = materialDAO.listar();
        modelo.addAttribute("materiales", materiales);
        modelo.addAttribute("material", new Material());
        return "materiales";
    }

    /**
     * Registra un nuevo material en la base de datos.
     */
    @PostMapping("/registrar")
    public String registrarMaterial(
            @ModelAttribute Material material,
            RedirectAttributes atributos) throws SQLException {

        if (material.getNombre() == null || material.getNombre().isBlank()
                || material.getCategoria() == null
                || material.getCategoria().isBlank()
                || material.getCantidad() < 0
                || material.getStockMinimo() < 0) {

            atributos.addFlashAttribute(
                    "error", "Verifica los datos. No se permiten nombres vacíos ni cantidades negativas.");

            return "redirect:/";
        }

        materialDAO.insertar(material);

        atributos.addFlashAttribute(
                "mensaje", "Material registrado correctamente.");

        return "redirect:/";
    }
}