import React from "react";
import { useEffect, useMemo, useState } from "react";

const datosIniciales = [
  { id: 1, nombre: "Tubería PVC", categoria: "Materiales", cantidad: 20, stockMinimo: 5 },
  { id: 2, nombre: "Cable eléctrico", categoria: "Materiales eléctricos", cantidad: 15, stockMinimo: 5 },
  { id: 3, nombre: "Guantes de seguridad", categoria: "Elementos de protección", cantidad: 8, stockMinimo: 10 }
];

const formularioVacio = { nombre: "", categoria: "", cantidad: "0", stockMinimo: "0" };

function EncabezadoInventario() {
  return (
    <header className="topbar">
      <div className="brand-mark" aria-hidden="true">I</div>
      <div>
        <p className="eyebrow">GESTIÓN OPERATIVA</p>
        <h1>Inventario de materiales</h1>
      </div>
      <span className="status-pill"><span /> Interfaz demostrativa</span>
    </header>
  );
}

function MensajeEstado({ mensaje, tipo, onCerrar }) {
  if (!mensaje) return null;
  return (
    <div className={`notice ${tipo}`} role="status">
      <span>{mensaje}</span>
      <button className="notice-close" type="button" onClick={onCerrar} aria-label="Cerrar mensaje">×</button>
    </div>
  );
}

function CampoFormulario({ etiqueta, id, tipo = "text", valor, onChange, requerido = false, minimo, error }) {
  return (
    <div className="field">
      <label htmlFor={id}>{etiqueta}{requerido && <span className="required"> *</span>}</label>
      <input
        id={id}
        name={id}
        type={tipo}
        value={valor}
        onChange={onChange}
        required={requerido}
        min={minimo}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${id}-error` : undefined}
      />
      {error && <small className="field-error" id={`${id}-error`}>{error}</small>}
    </div>
  );
}

function FormularioMaterial({ onRegistrar }) {
  const [formulario, setFormulario] = useState(formularioVacio);
  const [errores, setErrores] = useState({});

  function actualizar(evento) {
    const { name, value } = evento.target;
    setFormulario((actual) => ({ ...actual, [name]: value }));
    setErrores((actual) => ({ ...actual, [name]: "" }));
  }

  function enviar(evento) {
    evento.preventDefault();
    const nuevosErrores = {};
    if (!formulario.nombre.trim()) nuevosErrores.nombre = "Ingresa el nombre del material.";
    if (!formulario.categoria.trim()) nuevosErrores.categoria = "Ingresa la categoría.";
    if (formulario.cantidad === "" || Number(formulario.cantidad) < 0) nuevosErrores.cantidad = "La cantidad debe ser cero o mayor.";
    if (formulario.stockMinimo === "" || Number(formulario.stockMinimo) < 0) nuevosErrores.stockMinimo = "El stock mínimo debe ser cero o mayor.";
    setErrores(nuevosErrores);
    if (Object.keys(nuevosErrores).length) return;

    onRegistrar({
      nombre: formulario.nombre.trim(),
      categoria: formulario.categoria.trim(),
      cantidad: Number(formulario.cantidad),
      stockMinimo: Number(formulario.stockMinimo)
    });
    setFormulario(formularioVacio);
  }

  return (
    <form onSubmit={enviar} noValidate className="material-form">
      <div className="form-grid">
        <CampoFormulario etiqueta="Nombre del material" id="nombre" valor={formulario.nombre} onChange={actualizar} requerido error={errores.nombre} />
        <CampoFormulario etiqueta="Categoría" id="categoria" valor={formulario.categoria} onChange={actualizar} requerido error={errores.categoria} />
        <CampoFormulario etiqueta="Cantidad disponible" id="cantidad" tipo="number" minimo="0" valor={formulario.cantidad} onChange={actualizar} requerido error={errores.cantidad} />
        <CampoFormulario etiqueta="Stock mínimo" id="stockMinimo" tipo="number" minimo="0" valor={formulario.stockMinimo} onChange={actualizar} requerido error={errores.stockMinimo} />
      </div>
      <div className="form-actions">
        <span className="form-hint"><span className="required">*</span> Campos obligatorios</span>
        <button className="primary-button" type="submit"><span aria-hidden="true">＋</span> Registrar material</button>
      </div>
    </form>
  );
}

function ListaMateriales({ materiales, filtro }) {
  const filtrados = materiales.filter((material) =>
    `${material.nombre} ${material.categoria}`.toLowerCase().includes(filtro.toLowerCase())
  );

  if (!filtrados.length) {
    return <div className="empty-state"><span className="empty-icon">⌕</span><strong>No hay resultados</strong><p>Prueba otra búsqueda o registra un material.</p></div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr><th>Material</th><th>Categoría</th><th>Cantidad</th><th>Stock mínimo</th><th>Estado</th></tr>
        </thead>
        <tbody>
          {filtrados.map((material) => {
            const bajo = material.cantidad <= material.stockMinimo;
            return (
              <tr key={material.id}>
                <td><strong>{material.nombre}</strong><span className="row-id">ID #{material.id}</span></td>
                <td>{material.categoria}</td>
                <td><span className="quantity">{material.cantidad}</span></td>
                <td>{material.stockMinimo}</td>
                <td><span className={`stock-badge ${bajo ? "low" : "ok"}`}>{bajo ? "Reponer stock" : "Disponible"}</span></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function App() {
  const [materiales, setMateriales] = useState(() => {
    try {
      const guardados = localStorage.getItem("inventario-react-demo");
      return guardados ? JSON.parse(guardados) : datosIniciales;
    } catch {
      return datosIniciales;
    }
  });
  const [filtro, setFiltro] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [tipoMensaje, setTipoMensaje] = useState("success");

  useEffect(() => {
    localStorage.setItem("inventario-react-demo", JSON.stringify(materiales));
  }, [materiales]);

  const bajoStock = useMemo(
    () => materiales.filter((m) => m.cantidad <= m.stockMinimo).length,
    [materiales]
  );

  function registrar(material) {
    const siguienteId = materiales.reduce((max, m) => Math.max(max, m.id), 0) + 1;
    setMateriales((actuales) => [...actuales, { ...material, id: siguienteId }]);
    setTipoMensaje("success");
    setMensaje(`El material “${material.nombre}” se registró correctamente en esta demostración.`);
  }

  return (
    <div className="app-shell">
      <EncabezadoInventario />
      <main className="page-content">
        <section className="welcome-row">
          <div>
            <p className="eyebrow">PANEL PRINCIPAL</p>
            <h2>Resumen del inventario</h2>
            <p className="muted">Consulta las existencias y registra materiales en un solo lugar.</p>
          </div>
          <div className="date-chip">{new Date().toLocaleDateString("es-CO", { day: "2-digit", month: "long", year: "numeric" })}</div>
        </section>

        <section className="metrics" aria-label="Resumen">
          <article className="metric-card">
            <div className="metric-icon blue">▤</div>
            <div><span className="metric-label">Materiales registrados</span><strong>{materiales.length}</strong><small>Registros en esta demostración</small></div>
          </article>
          <article className="metric-card">
            <div className="metric-icon amber">!</div>
            <div><span className="metric-label">Alertas de stock</span><strong>{bajoStock}</strong><small>Materiales en o bajo el mínimo</small></div>
          </article>
        </section>

        <MensajeEstado mensaje={mensaje} tipo={tipoMensaje} onCerrar={() => setMensaje("")} />

        <section className="panel">
          <div className="panel-heading">
            <div><h3>Materiales registrados</h3><p>Consulta y filtra los elementos del inventario.</p></div>
            <label className="search-box"><span aria-hidden="true">⌕</span><input aria-label="Buscar materiales" value={filtro} onChange={(e) => setFiltro(e.target.value)} placeholder="Buscar material..." /></label>
          </div>
          <ListaMateriales materiales={materiales} filtro={filtro} />
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div><h3>Registrar material</h3><p>Completa los datos para agregar un registro a la demostración.</p></div>
          </div>
          <FormularioMaterial onRegistrar={registrar} />
        </section>
        <p className="demo-note"><strong>Nota:</strong> esta versión React es una demostración independiente. Los registros se guardan en el almacenamiento local del navegador y todavía no se conectan a la base de datos SQLite ni al backend Spring Boot.</p>
      </main>
      <footer className="footer">Sistema de inventario · Front-end React · Evidencia GA7-220501096-AA4-EV03</footer>
    </div>
  );
}