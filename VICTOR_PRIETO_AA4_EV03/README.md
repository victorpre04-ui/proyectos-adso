# Inventario de materiales — Front-end React

Evidencia SENA: **GA7-220501096-AA4-EV03**  
Aprendiz: Víctor Prieto  
Instructora: Adriana Rangel  
Fecha: 20 de octubre de 2026

## Descripción
Interfaz demostrativa de inventario desarrollada con React y Vite. Incluye resumen de materiales, tabla con búsqueda, formulario de registro, validaciones de campos, avisos de estado y diseño adaptable a pantallas pequeñas.

## Requisito
- Node.js y npm instalados.

## Ejecución
Desde esta carpeta:

```bash
npm install
npm run dev
```

Vite mostrará una dirección local, normalmente `http://localhost:5173/`.

## Construcción de producción
```bash
npm run build
```

## Alcance y limitación
Esta interfaz es una demostración independiente. Los registros se guardan en `localStorage` del navegador. Todavía no está conectada a la base de datos SQLite ni al backend Spring Boot existente; esa integración requiere que el backend exponga endpoints HTTP.

## Estructura
- `src/main.jsx`: punto de entrada React.
- `src/App.jsx`: componentes y lógica de interfaz.
- `src/styles.css`: estilos responsivos.
- `index.html`: documento HTML base.
