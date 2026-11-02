# Natara · by Samanat

Software de gestión para pequeños negocios (panaderías, farmacias, minimercados, papelerías): inventario, caja, ingresos y egresos, estadísticas y una consola de administración para Samanat.

## Demo

- **App real (clientes):** https://samanat2026.github.io/natara/
- **Demo para mostrar:** https://samanat2026.github.io/natara/demo/

`index.html` es la app real y `demo/index.html` la demo, generadas desde el mismo código (`window.NATARA_MODE`). La demo trae datos de ejemplo y cuentas de prueba; la app real arranca vacía, solo con la cuenta de Samanat.

Los datos de la demo se guardan en el navegador (`localStorage`). La app real usa **Firebase** (proyecto `natara-96555`): Authentication con correo y contraseña, y Firestore en `southamerica-east1`. Las reglas de seguridad están en [`firestore.rules`](firestore.rules) y se pegan en Firebase → Firestore → Reglas.

### Cuentas de ejemplo

Contraseña de todas las cuentas: `Natara2026*`. La consola de Samanat (superadmin) no existe en la demo; solo en la app real.

| Correo | Rol | Qué ve |
|---|---|---|
| marta@laespiga.co | Dueña · Panadería La Espiga | Plan Total + Recetas y combos |
| juan@laespiga.co | Cajero · Panadería La Espiga | Caja + permisos: inventario, costos, recetas, proveedores y fiados |
| laura@laespiga.co | Cajera · Panadería La Espiga | Sin permisos extra: solo vende y ve sus propias ventas |
| pedro@laespiga.co | Cajero desactivado | Prueba el mensaje de usuario desactivado |
| carlos@vidasana.co | Dueño · Droguería Vida Sana | Plan Pro |
| pacho@minimercado.co | Dueño · Minimercado Don Pacho | Plan Básico |
| andrea@arcoiris.co | Dueña · Papelería Arcoíris | Cuenta suspendida (pantalla de bloqueo) |

## Planes (COP, IVA no incluido)

| Plan | Mensual | Anual (12 meses por 10) | Módulos |
|---|---|---|---|
| Básico | $59.900 | $599.000 | Inventario, Caja y ventas |
| Pro | $109.900 | $1.099.000 | + Ingresos y egresos, Estadísticas, Empleados |
| Total | $159.900 | $1.599.000 | + Fiados y clientes, Proveedores |

### Módulos sueltos y complementos

| Módulo | Precio mensual |
|---|---|
| Inventario | $29.900 |
| Caja y ventas | $29.900 |
| Ingresos y egresos | $24.900 |
| Estadísticas | $24.900 |
| Empleados (con permisos) | $19.900 |
| Fiados y clientes | $22.900 |
| Proveedores | $19.900 |
| Recetas y combos (complemento) | $10.000 |
| Lector de código de barras (complemento, no se promociona) | $14.900 |

Implementación opcional: $180.000 una sola vez (carga de inventario, configuración y capacitación).

## Pagos con llave Bre-B

- **Cuota:** el dueño entra a *Mi plan → Pagar mi cuota*, ve la llave, el valor exacto y una referencia (NAT-XXXXXX), paga desde su banco y toca *Ya pagué*. Mientras Samanat revisa, la cuenta no se bloquea (hasta 7 días).
- **Compra desde la demo:** *Contratar este plan* → datos del negocio → pago con la llave → *Ya pagué*. El pedido llega a la consola.
- **Aprobación:** en la consola, *Pagos y solicitudes → Aprobar*. Una renovación extiende la fecha de vencimiento; una compra nueva crea el negocio y el usuario y envía el correo de bienvenida.
- **Aviso a Samanat:** cada pago reportado (cuota o negocio nuevo) envía un correo a samanat2026@gmail.com con una segunda plantilla de EmailJS (`{{to_email}}`, `{{subject}}`, `{{message}}`). Es el único correo que sale desde la demo.
- La llave, el titular y la plantilla del aviso se cambian en *Planes y precios → Cobros con llave Bre-B*.

## Correo de bienvenida

Al crear un cliente se genera una contraseña temporal y se envía por correo con [EmailJS](https://www.emailjs.com/) (configurable en Planes y precios → Envío de correos). En el primer ingreso el cliente debe crear su propia contraseña.

## Próximos pasos

- Versión de producción en Angular + Firebase (Auth, Firestore, Hosting): cuentas reales entre dispositivos y actividad en vivo de todos los clientes.
- Facturación electrónica DIAN.
- Módulo de producción y recetas para panaderías.
- Producto 2: agendamiento de citas para salones de uñas por WhatsApp.
