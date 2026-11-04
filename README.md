# Natara · by Samanat

Software de gestión para pequeños negocios (panaderías, farmacias, minimercados, papelerías, restaurantes): inventario, caja, ingresos y egresos, estadísticas y una consola de administración para Samanat.

## Demo

- **App real (clientes):** https://samanat2026.github.io/natara/
- **Demo para mostrar:** https://samanat2026.github.io/natara/demo/

`index.html` es la app real y `demo/index.html` la demo, generadas desde el mismo código (`window.NATARA_MODE`). Solo se edita `index.html`; después `python3 tools/build.py` genera `demo/`, `consola-demo/` y la copia en `docs/`. La demo trae datos de ejemplo y cuentas de prueba; la app real arranca vacía, solo con la cuenta de Samanat.

Los datos de la demo se guardan en el navegador (`localStorage`). La app real usa **Firebase** (proyecto `natara-96555`): Authentication con correo y contraseña, y Firestore en `southamerica-east1`. Las reglas de seguridad están en [`firestore.rules`](firestore.rules) y se pegan en Firebase → Firestore → Reglas.

### Cuentas de ejemplo

Contraseña de todas las cuentas: `Natara2026*`. La consola de Samanat (superadmin) no existe en la demo; solo en la app real.

| Correo | Rol | Qué ve |
|---|---|---|
| marta@laespiga.co | Dueña · Panadería La Espiga | Plan Total (todos los módulos) |
| juan@laespiga.co | Cajero · Panadería La Espiga | Caja + permisos: inventario, costos, recetas, proveedores y fiados |
| laura@laespiga.co | Cajera · Panadería La Espiga | Sin permisos extra: solo vende y ve sus propias ventas |
| pedro@laespiga.co | Cajero desactivado | Prueba el mensaje de usuario desactivado |
| carlos@vidasana.co | Dueño · Droguería Vida Sana | Plan Pro |
| pacho@minimercado.co | Dueño · Minimercado Don Pacho | Plan Básico |
| andrea@arcoiris.co | Dueña · Papelería Arcoíris | Cuenta suspendida (pantalla de bloqueo) |
| diana@elfogon.co | Dueña · Restaurante El Fogón Paisa | Plan Total, con 12 mesas y 4 ocupadas |
| andres@elfogon.co | Cajero · El Fogón | Entra a las mesas y cobra por persona |
| camila@elfogon.co | Mesera · El Fogón | Solo ve las mesas: abre, agrega productos y pide la cuenta. No cobra |
| sebastian@elfogon.co | Mesero · El Fogón | Igual que Camila, pero con el permiso *Cobrar las mesas* |

## Planes (COP, IVA no incluido)

| Plan | Mensual | Anual (12 meses por 10) | Módulos |
|---|---|---|---|
| Básico | $59.900 | $599.000 | Inventario, Caja y ventas |
| Pro | $109.900 | $1.099.000 | + Ingresos y egresos, Estadísticas, Empleados |
| Total | $159.900 | $1.599.000 | **Todo:** + Fiados y clientes, Proveedores, Mesas y meseros, Recetas y combos, Puntos y fidelización y Lector de código de barras |

### Módulos sueltos y complementos

Los complementos se suman a Básico o Pro; el plan Total ya los incluye todos (también los módulos que se agreguen después).

| Módulo | Precio mensual |
|---|---|
| Inventario | $29.900 |
| Caja y ventas | $29.900 |
| Ingresos y egresos | $24.900 |
| Estadísticas | $24.900 |
| Empleados (con permisos) | $19.900 |
| Fiados y clientes | $22.900 |
| Proveedores | $19.900 |
| Mesas y meseros (restaurantes y cafeterías) | $29.900 |
| Recetas y combos (complemento) | $10.000 |
| Lector de código de barras (complemento, no se promociona) | $14.900 |
| Puntos y fidelización (complemento) | $5.000 |

Implementación opcional: $180.000 una sola vez (carga de inventario, configuración y capacitación).

## Puntos y fidelización

Complemento de $5.000/mes que paga el dueño del negocio (incluido en el plan Total); solo aparece si lo tiene activo. Para el cliente final afiliarse es gratis.

- **Afiliación:** en la caja se escribe la cédula; si no está afiliado, *Afiliarlo ahora* pide nombre, celular y la autorización de datos (Ley 1581 de 2012).
- **Acumular:** cada venta suma `floor(total pagado / monto por punto)` puntos. Las ventas fiadas no suman.
- **Usar:** con el mínimo de puntos, *Usar N puntos* descuenta `N × valor del punto` sin pasarse del total. El total de la venta (caja, cierre y reportes) es lo que el cliente pagó en dinero.
- **Vencimiento:** los puntos se guardan por lotes y vencen a los N meses; al usarlos se gastan primero los más viejos.
- **Anular una venta** quita los puntos ganados y devuelve los usados.
- **Configuración (dueño → Puntos → Configurar):** por defecto 1 punto por cada $1.000, cada punto vale $7, mínimo 100 para usarlos, vencen a los 12 meses, 0 de bienvenida.
- Datos en Firestore: `tenants/{tid}/members` (afiliados con sus lotes), `tenants/{tid}/pmoves` (historial) y `tenants/{tid}/settings/fid_{tid}` (configuración).

## Mesas y meseros

Módulo de $29.900/mes para restaurantes, cafeterías y panaderías con mesas (incluido en el plan Total). Solo se ofrece en *Mi plan* a negocios de comida; a los demás no les aparece.

- **Mesas:** el dueño escribe cuántas mesas tiene y se crean como Mesa 1, Mesa 2…; en *Configurar mesas* las renombra (Terraza 1, Barra…), agrega o elimina (las ocupadas no se eliminan).
- **Mapa de mesas:** libres (punteadas), ocupadas (verde) y las que pidieron la cuenta (amarillo), con el tiempo abierta, lo que falta por cobrar, las personas y quién la atiende.
- **Atender:** se abre la mesa (personas opcional) y se tocan los productos para agregarlos; con − y + se corrigen las cantidades. Se puede *Cambiar de mesa* y *Pedir la cuenta*. En el celular, la barra *Ver cuenta* muestra el total.
- **Cobro por persona:** *Cobrar* muestra lo pendiente; se marca lo que paga esa persona o grupo (o *Seleccionar todo*) y se cobra con el mismo panel de la caja (efectivo, transferencia, datáfono, fiado y puntos). Lo no pagado sigue en la mesa; cuando se paga todo, la mesa se libera sola. El recibo dice la mesa.
- **Meseros:** son empleados con puesto *Mesero(a)* (se elige al crearlos o en *Permisos*). Solo ven *Mesas* y la guía. Por defecto **no cobran**: el cobro lo hace la caja. Los cajeros del restaurante entran directo a *Mesas*.
- **Permiso *Cobrar las mesas* (solo meseros):** el dueño lo activa por mesero al crearlo o en *Permisos*. Con el permiso, el mesero cobra desde la mesa, la venta queda a su nombre, ve sus cobros en *Ventas* y entrega el dinero en la caja. No puede abrir ni cerrar la caja: si está cerrada, la app le dice que se la pida al cajero. Se guarda como `mesa_cobrar` en `perms`.
- **Inventario:** el stock se descuenta al cobrar (no al pedir). Anular una venta de mesa devuelve lo pagado a la mesa.
- **Cómo se ven los pagos divididos:** cada persona o grupo que paga es una venta propia (con su número, vendedor y medio de pago), con los campos `mesa`, `tab`, `mesaN` (número de pago en esa mesa) y `mesaRest` (lo que quedó pendiente).
  - *Ventas:* etiqueta *Mesa 2 · pago 3*, filtro *Solo mesas / Solo caja* y búsqueda por nombre de mesa; el Excel trae la columna Mesa.
  - *Recibo:* número de pago, lo que queda pendiente (o *mesa saldada*) y la lista de todos los pagos de esa mesa con el total pagado.
  - *Ingresos y egresos:* cada día se separa en *Ventas en mesas* y *Ventas en caja*, y el total de ingresos dice cuánto vino de mesas. Cierre de caja y estadísticas las cuentan como cualquier venta.
- **Datos en Firestore:** `tenants/{tid}/tables` (mesas), `tenants/{tid}/tabs` (cuenta de una mesa: `table`, `openedBy`, `guests`, `bill`, `open`) y `tenants/{tid}/tablines` (un documento por producto pedido: `tab`, `qty`, `paid`, `by`). Cada producto es un documento aparte para que el mesero agregue mientras la caja cobra sin pisarse. La app solo escucha las cuentas abiertas (`open == true`).
- **Reglas:** `tabs` y `tablines` las escribe cualquier usuario del negocio que tenga el módulo; `tables`, solo el dueño. El mesero sigue siendo `role: 'cajero'` (con `puesto: 'mesero'`), así que no cambian las reglas de usuarios. Hay que volver a pegar `firestore.rules` en Firebase.

## Caja por categorías

Opción **sin costo** que Samanat activa por negocio, solo si el cliente la pide (no todos la quieren). Apagada, la caja sigue igual que siempre.

- **Activar:** consola → *Clientes* → columna *Caja por categorías*. Al encenderla, el dueño recibe un mensaje. El dueño la puede pedir desde *Mi plan* (botón de WhatsApp).
- **Categorías:** el dueño (o un empleado con permiso de editar inventario) las crea en *Inventario → Categorías*: agregar, renombrar, ordenar con flechas y eliminar. Si los productos ya traían categoría (por ejemplo del Excel), *Agregarlas* las crea de una vez.
- **Unir productos:** en cada categoría, *Elegir productos* muestra la lista con buscador para marcar varios a la vez. También se elige al crear o editar un producto (o una receta/combo), con la opción *+ Nueva categoría…*.
- **En la caja:** arriba salen las categorías como botones (*Más vendidos*, Panes, Bebidas…, *Sin categoría*). Al tocar una salen todos sus productos; la búsqueda sigue buscando en todo el inventario. Las categorías vacías no aparecen.
- Renombrar una categoría actualiza sus productos; eliminarla deja los productos como “Sin categoría” (no se borran). Apagar la opción no borra nada.
- Datos en Firestore: `tenants/{tid}.catPos` (encendida o no) y `tenants/{tid}/cats` (`name`, `order`). El producto guarda el nombre de su categoría en `cat`, como antes.
- **Reglas:** se agregó `cats` a lo que puede escribir un empleado con permiso `inv_edit`. Hay que volver a pegar `firestore.rules` en Firebase.

## Pagos con llave Bre-B

- **Cuota:** el dueño entra a *Mi plan → Pagar mi cuota*, ve la llave, el valor exacto y una referencia (NAT-XXXXXX), paga desde su banco y toca *Ya pagué*. Mientras Samanat revisa, la cuenta no se bloquea (hasta 7 días).
- **Compra desde la demo:** *Contratar este plan* → datos del negocio → pago con la llave → *Ya pagué*. El pedido llega a la consola.
- **Módulos e implementación:** en *Mi plan* cada módulo tiene *Contratar*: el dueño paga el primer mes (o los $180.000 de la implementación) con la llave y toca *Ya pagué*. Al aprobarlo se activa al instante y se suma a la cuota. En la demo se puede agregar cualquier módulo suelto al plan.
- **Aprobación:** en la consola, *Pagos y solicitudes → Aprobar*. Una renovación extiende la fecha de vencimiento; una compra nueva crea el negocio y el usuario y envía el correo de bienvenida.
- **Aviso a Samanat:** cada pago reportado (cuota o negocio nuevo) envía un correo a samanat2026@gmail.com con una segunda plantilla de EmailJS (`{{to_email}}`, `{{subject}}`, `{{message}}`). Es el único correo que sale desde la demo.
- **QR:** la consola permite subir el QR oficial de la llave (generado en la app del banco); se muestra junto al valor y la referencia.
- La llave, el titular, el QR y la plantilla del aviso se cambian en *Planes y precios → Cobros con llave Bre-B*.

## Correo de bienvenida

Al crear un cliente se genera una contraseña temporal y se envía por correo con [EmailJS](https://www.emailjs.com/) (configurable en Planes y precios → Envío de correos). En el primer ingreso el cliente debe crear su propia contraseña.

## Próximos pasos

- Versión de producción en Angular + Firebase (Auth, Firestore, Hosting): cuentas reales entre dispositivos y actividad en vivo de todos los clientes.
- Facturación electrónica DIAN (cada pago parcial de una mesa debe salir con su propia factura).
- Mesas: comandas a cocina, unir mesas y dividir en partes iguales.
- Módulo de producción y recetas para panaderías.
- Producto 2: agendamiento de citas para salones de uñas por WhatsApp.
