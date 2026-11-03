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
| marta@laespiga.co | Dueña · Panadería La Espiga | Plan Total (todos los módulos) |
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
| Total | $159.900 | $1.599.000 | **Todo:** + Fiados y clientes, Proveedores, Recetas y combos, Puntos y fidelización y Lector de código de barras |

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
- Facturación electrónica DIAN.
- Módulo de producción y recetas para panaderías.
- Producto 2: agendamiento de citas para salones de uñas por WhatsApp.
