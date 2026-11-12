# Natara · by Samanat

Software de gestión para pequeños negocios (panaderías, farmacias, minimercados, papelerías, restaurantes): inventario, caja, ingresos y egresos, estadísticas y una consola de administración para Samanat.

## Demo

- **App real (clientes):** https://natara.com.co/
- **Demo para mostrar:** https://natara.com.co/demo/
- **Hosting:** Cloudflare Pages, conectado a este repositorio: cada push a `main` publica la carpeta `docs/` en https://natara.com.co/. Antes de subir: `python3 tools/build.py` y `python3 tools/check.py`.
- Los enlaces que ven los clientes (correos, WhatsApp, "ir a la app") siempre usan https://natara.com.co/ (`SITE_URL` en `index.html`); solo en pruebas locales (localhost) usan la dirección local.

`index.html` es la app real y `demo/index.html` la demo, generadas desde el mismo código (`window.NATARA_MODE`). Solo se edita `index.html`; después `python3 tools/build.py` genera `demo/`, `consola-demo/` y la copia en `docs/`. La demo trae datos de ejemplo y cuentas de prueba; la app real arranca vacía, solo con la cuenta de Samanat.

Los datos de la demo se guardan en el navegador (`localStorage`). La app real usa **Firebase** (proyecto `natara-96555`): Authentication con correo y contraseña, y Firestore en `southamerica-east1`. Las reglas de seguridad están en [`firestore.rules`](firestore.rules) y se pegan en Firebase → Firestore → Reglas.

### Consumo de Firestore (plan gratis)

Para no gastar la cuota diaria, la app real solo escucha en vivo lo de hoy: ventas, gastos, compras, cajas y puntos del día, más mesas abiertas, productos, clientes y fiados. Lo anterior se pide una sola vez al abrir la pantalla que lo usa (Ventas, Estadísticas, Ingresos y egresos, Cierre, Proveedores, Puntos). El kardex ya no se escucha: se consultan los últimos 30 movimientos al abrir *Ajustar stock*. Los meseros sin permiso de cobro solo escuchan mesas, productos y ventas del día. La presencia se actualiza cada 10 minutos.

El kardex necesita un índice compuesto, definido en [`firestore.indexes.json`](firestore.indexes.json): Firebase → Firestore → Índices → Compuesto → Crear índice, colección `kardex`, campos `pid` Ascendente y `at` Descendente, ámbito Colección. Mientras no exista, la app trae los movimientos de los últimos 60 días y los filtra.

### Reglas: qué puede hacer cada quien (actualizado el 5 de noviembre de 2026)

**Hay que volver a pegar [`firestore.rules`](firestore.rules) en Firebase → Firestore → Reglas → Publicar.**

- **Ventas, cajas y kardex:** cualquier usuario del negocio los crea, pero solo el dueño los cambia o los borra. Un empleado solo puede confirmar una transferencia, anular una venta si tiene el permiso *Anular ventas* (queda guardado quién, cuándo y por qué) y cerrar una caja abierta.
- **Pago reportado ("Ya pagué"):** la fecha del reporte tiene que ser la de ese momento, y la cuenta sigue activa como máximo 10 días después del vencimiento (3 de gracia + 7 de revisión), aunque el dueño reporte varias veces.

### Revisión automática

`python3 tools/check.py` revisa que el JavaScript de las páginas no tenga errores de sintaxis y que `demo/`, `consola-demo/` y `docs/` estén generados desde `index.html`. GitHub lo corre solo en cada push (`.github/workflows/revisar.yml`).

### Alerta de cuota por WhatsApp

`tools/alerta_cuota.py` está **apagado** (solo se corre a mano en Actions): las métricas de Firestore que usa solo existen en el plan Blaze. Cuando se encienda, corre cada hora (`.github/workflows/alerta-cuota.yml`). Consulta en Google Cloud Monitoring cuántas lecturas, escrituras y borrados lleva Firestore hoy y avisa por WhatsApp (CallMeBot) al pasar el 80 %, el 90 % y el 95 % de la cuota gratis (50.000 lecturas, 20.000 escrituras y 20.000 borrados al día). Cada aviso sale una vez al día; la cuota se reinicia a la medianoche del Pacífico (2 o 3 a. m. en Colombia). Necesita los secretos `GCP_SA_KEY`, `CALLMEBOT_PHONE` y `CALLMEBOT_APIKEY`. Para probarlo: Actions → *Alerta de cuota de Firebase* → *Run workflow*.

### Cuentas de ejemplo

Contraseña de todas las cuentas: `Natara2026*`. La consola de Samanat (superadmin) no existe en la demo; solo en la app real.

| Correo | Rol | Qué ve |
|---|---|---|
| pacho@minimercado.co | Dueño · Minimercado Don Pacho | Plan Premium (todo para tiendas): fiados, proveedores, combos, puntos encendidos y caja por categorías |
| yuliana@minimercado.co | Cajera · Don Pacho | Caja + permisos: inventario, costos, recetas, proveedores y fiados |
| brayan@minimercado.co | Cajero · Don Pacho | Sin permisos extra: solo vende y ve sus propias ventas |
| kevin@minimercado.co | Cajero desactivado | Prueba el mensaje de usuario desactivado |
| carlos@vidasana.co | Dueño · Droguería Vida Sana | Plan Pro |
| marta@laespiga.co | Dueña · Panadería La Espiga | Plan Básico: inventario, caja y apertura y cierre, sin empleados |
| andrea@arcoiris.co | Dueña · Papelería Arcoíris | Cuenta suspendida (pantalla de bloqueo). Solo aparece en la consola de demo, no en la demo de clientes |
| diana@elfogon.co | Dueña · Restaurante El Fogón Paisa | Plan Restaurante, con 12 mesas y 4 ocupadas; puntos incluidos pero apagados |
| andres@elfogon.co | Cajero · El Fogón | Entra a las mesas y cobra por persona |
| camila@elfogon.co | Mesera · El Fogón | Solo ve las mesas: abre, agrega productos y pide la cuenta. No cobra |
| sebastian@elfogon.co | Mesero · El Fogón | Igual que Camila, pero con el permiso *Cobrar las mesas* |

## Planes (COP, precio final: Samanat no cobra IVA)

| Plan | Mensual | Anual (12 meses por 10) | Módulos |
|---|---|---|---|
| Básico | $59.900 | $599.000 | Inventario, Caja y ventas |
| Pro | $109.900 | $1.099.000 | + Ingresos y egresos, Estadísticas, Empleados |
| Premium | $159.900 | $1.599.000 | **Todo para tiendas:** + Fiados y clientes, Proveedores, Recetas y combos, Puntos y fidelización y Lector de código de barras |
| Restaurante | $179.900 | $1.799.000 | **Todo lo de Premium + Mesas y meseros** |

El plan Premium se llamaba *Total* (en el código su id sigue siendo `total`, para no tocar a los clientes que ya lo tienen). Premium ya no incluye Mesas; los negocios que lo tenían antes la pierden sola (campo `v2` del negocio) a menos que Samanat se la active aparte. Premium + Mesas suelto saldría a $189.800, así que el plan Restaurante ($179.900) es lo que conviene ofrecerle a un restaurante; *Mi plan* se lo sugiere al dueño.

### Módulos sueltos y complementos

Los complementos se suman a cualquier plan. Premium incluye todos los módulos menos Mesas, y Restaurante los incluye todos (en ambos casos también los que se agreguen después).

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
| Lector de código de barras: cámara o USB (complemento, no se promociona) | $14.900 |
| Puntos y fidelización (complemento) | $5.000 |

Implementación opcional: $180.000 una sola vez (carga de inventario, configuración y capacitación).

## Puntos y fidelización

Complemento de $5.000/mes que paga el dueño del negocio (incluido en Premium y Restaurante). Para el cliente final afiliarse es gratis.

- **Encender y apagar:** aunque esté en el plan, arranca **apagado**. El dueño lo enciende en *Mi plan → Puntos y fidelización → Encender* (y lo apaga ahí o en *Puntos*). Apagado, no aparece en la caja, en el cobro de mesas, en el menú ni en la guía, y no se borra nada. Se guarda en `on` de `tenants/{tid}/settings/fid_{tid}`; los negocios que ya lo usaban (con configuración o afiliados) siguen encendidos.

- **Afiliación:** en la caja se escribe la cédula; si no está afiliado, *Afiliarlo ahora* pide nombre, celular y la autorización de datos (Ley 1581 de 2012).
- **Acumular:** cada venta suma `floor(total pagado / monto por punto)` puntos. Las ventas fiadas no suman.
- **Usar:** con el mínimo de puntos, *Usar N puntos* descuenta `N × valor del punto` sin pasarse del total. El total de la venta (caja, cierre y reportes) es lo que el cliente pagó en dinero.
- **Vencimiento:** los puntos se guardan por lotes y vencen a los N meses; al usarlos se gastan primero los más viejos.
- **Anular una venta** quita los puntos ganados y devuelve los usados.
- **Configuración (dueño → Puntos → Configurar):** por defecto 1 punto por cada $1.000, cada punto vale $7, mínimo 100 para usarlos, vencen a los 12 meses, 0 de bienvenida.
- Datos en Firestore: `tenants/{tid}/members` (afiliados con sus lotes), `tenants/{tid}/pmoves` (historial) y `tenants/{tid}/settings/fid_{tid}` (configuración).

## Lector de código de barras (cámara o USB)

Complemento de $14.900/mes (incluido en Premium y Restaurante). Samanat lo activa por negocio en la consola. Con él activo, el negocio puede escanear de **dos formas, sin configurar nada**:

- **Cámara del celular o del computador (gratis):** botón *Cámara* en la búsqueda de la Caja, las Mesas, el Inventario y las compras a proveedores, y botón de cámara junto al campo *Código de barras* del producto. En la caja y las mesas el escáner se queda abierto: cada producto que se lee entra solo a la venta, con pitido y vibración. Mientras el mismo código siga frente a la cámara no se suma dos veces; para otro igual se retira y se vuelve a apuntar. Si el código no existe, el dueño lo puede crear ahí mismo.
  - Motor: el `BarcodeDetector` del navegador (Chrome en Android) y, donde no existe (iPhone, Firefox, computador), ZXing (`@zxing/library` 0.21.3 desde jsDelivr), que solo se descarga la primera vez que se abre la cámara. Lee EAN-13, EAN-8, UPC, Code 128, Code 39, ITF y QR.
  - Necesita HTTPS (natara.com.co ya lo es) y que la persona dé permiso de cámara.
- **Cantidad al leer un producto:** en la Caja, al leer un código con el lector USB aparece arriba *Arroz 1 kg · ¿Cuántos?* con el número listo para escribir: se escribe la cantidad y Enter. Si en vez de eso se lee otro producto, el primero queda con 1 y sigue el nuevo. Con la cámara, el último producto leído trae − y + y un campo para escribir la cantidad en la misma pantalla del lector.
- **Lector USB o Bluetooth:** funciona como un teclado. En la Caja, las Mesas (dentro de una mesa) y el Inventario no hace falta tocar el campo de búsqueda: Natara reconoce las teclas rápidas que terminan en Enter y agrega el producto. Si el cursor está en un campo (por ejemplo *Código* del producto), el código se escribe ahí.

Los códigos de la demo son inventados y no tienen dígito de control válido, así que con la cámara solo se leen productos reales; en la demo se puede probar escaneando cualquier producto empacado y creándolo con *Crearlo*.

## Sin vender lo que no hay

Si el negocio tiene el módulo de Inventario, la caja y las mesas no dejan vender más de lo que hay: el inventario (o lo que alcanzan los ingredientes de una receta) menos lo que ya está pedido y sin cobrar en las mesas abiertas. Se revisa al agregar el producto, al subir la cantidad y otra vez al cobrar. El aviso dice cuántos quedan.

## Botón Atrás

Cada pantalla queda en el historial del navegador (`history.pushState` desde `render()`), así que el botón *Atrás* del celular o del navegador vuelve a la pantalla anterior en vez de cerrar la app: de un cobro a la mesa, de la mesa al mapa, de Ventas a Inicio. Si hay una ventana abierta o el menú del celular, *Atrás* solo los cierra. *Atrás* nunca vuelve a la sesión de otro usuario ni entra de nuevo después de cerrar sesión.

## Mesas y meseros

Módulo de $29.900/mes para restaurantes, cafeterías y panaderías con mesas (incluido en el plan Restaurante; se puede agregar a cualquier otro plan). Si el negocio no tiene el módulo o no ha creado mesas, el cajero trabaja como siempre en la Caja. Solo se ofrece en *Mi plan* a negocios de comida; a los demás no les aparece.

- **Mesas:** el dueño escribe cuántas mesas tiene y se crean como Mesa 1, Mesa 2…; en *Configurar mesas* las renombra (Terraza 1, Barra…), agrega o elimina (las ocupadas no se eliminan).
- **Mapa de mesas:** libres (punteadas), ocupadas (verde) y las que pidieron la cuenta (amarillo), con el tiempo abierta, lo que falta por cobrar, las personas y quién la atiende.
- **Atender:** se abre la mesa (personas opcional) y se tocan los productos para agregarlos; con − y + se corrigen las cantidades. Se puede *Cambiar de mesa* y *Pedir la cuenta*. En el celular, la barra *Ver cuenta* muestra el total.
- **Cobro por persona:** *Cobrar* muestra lo pendiente; se marca lo que paga esa persona o grupo (o *Seleccionar todo*) y se cobra con el mismo panel de la caja (efectivo, transferencia, datáfono, fiado y puntos). Lo no pagado sigue en la mesa; cuando se paga todo, la mesa se libera sola. El recibo dice la mesa.
- **Meseros:** son empleados con puesto *Mesero(a)* (se elige al crearlos o en *Permisos*). Solo ven *Mesas* y la guía. Por defecto **no cobran**: el cobro lo hace la caja. Los cajeros del restaurante entran directo a *Mesas*.
- **Permiso *Cobrar las mesas* (solo meseros):** el dueño lo activa por mesero al crearlo o en *Permisos*. Con el permiso, el mesero cobra desde la mesa, la venta queda a su nombre, ve sus cobros en *Ventas* y entrega el dinero en la caja. No puede abrir ni cerrar la caja: si está cerrada, la app le dice que se la pida al cajero. Se guarda como `mesa_cobrar` en `perms`.
- **Inventario:** el stock se descuenta al cobrar (no al pedir). Anular una venta de mesa devuelve lo pagado a la mesa.
- **Dos formas de cobrar una mesa:** *Por productos* (se marca lo que paga cada persona) o *Partes iguales* (la cuenta pendiente entre N personas). En partes iguales cada parte paga la misma fracción de cada producto pendiente, así el inventario y las estadísticas cuadran; la última parte paga exactamente lo que falte. La mesa guarda `split: {n, done}` y cada venta `split: {n, from, to}`; el recibo la muestra como *Parte 1 de 3 de la cuenta*.
- **Cómo se ven los pagos divididos:** cada persona o grupo que paga es una venta propia (con su número, vendedor y medio de pago), con los campos `mesa`, `tab`, `mesaN` (número de pago en esa mesa) y `mesaRest` (lo que quedó pendiente).
  - *Ventas:* etiqueta *Mesa 2 · pago 3*, filtro *Solo mesas / Solo caja* y búsqueda por nombre de mesa; el Excel trae la columna Mesa.
  - *Recibo:* solo lo que pagó esa persona o grupo y su total (no muestra los pagos de los demás). Encima del recibo, solo en la app, el cajero ve si la mesa sigue abierta y cuánto falta; al abrir la venta desde Ventas también ve los otros pagos de esa mesa.
  - *Ingresos y egresos:* cada día se separa en *Ventas en mesas* y *Ventas en caja*, y el total de ingresos dice cuánto vino de mesas. Cierre de caja y estadísticas las cuentan como cualquier venta.
- **Datos en Firestore:** `tenants/{tid}/tables` (mesas), `tenants/{tid}/tabs` (cuenta de una mesa: `table`, `openedBy`, `guests`, `bill`, `open`) y `tenants/{tid}/tablines` (un documento por producto pedido: `tab`, `qty`, `paid`, `by`). Cada producto es un documento aparte para que el mesero agregue mientras la caja cobra sin pisarse. La app solo escucha las cuentas abiertas (`open == true`).
- **Reglas:** `tabs` y `tablines` las escribe cualquier usuario del negocio que tenga el módulo; `tables`, solo el dueño. El mesero sigue siendo `role: 'cajero'` (con `puesto: 'mesero'`), así que no cambian las reglas de usuarios. Hay que volver a pegar `firestore.rules` en Firebase.

## Mi negocio

Sección nueva del menú, solo para el dueño (*Cuenta → Mi negocio*).

- **Datos para el recibo:** razón social o nombre del titular, NIT o cédula (el dígito de verificación se calcula solo con el algoritmo de la DIAN), dirección, ciudad, teléfono, correo, régimen (responsable o no responsable de IVA) y un mensaje al pie. Salen arriba en todos los recibos, también en los pagos divididos de mesas, con una vista previa en vivo. Si hay NIT, el recibo aclara que es un *documento de control interno, no factura electrónica*. Se guardan en `tenants/{tid}/settings/biz_{tid}`.
- **Funciones que el dueño enciende o apaga** (`tenants/{tid}/settings/opts_{tid}`; al apagar no se borra nada):
  - *Caja por categorías:* sin costo y en cualquier plan; el dueño la enciende solo. Si nunca la ha tocado, vale lo que Samanat dejó en la consola.
  - *Puntos y fidelización:* si está en su plan (arranca apagado).
  - *Lector de código de barras:* si lo tiene; apagado, la caja busca solo por nombre.
- No hay que cambiar las reglas de Firebase: el dueño ya podía escribir en `settings`.

## Imprimir recibos

Opción **sin costo** que arranca **apagada en todos los planes**. Se enciende o apaga en dos lugares:

- **Consola de Samanat:** *Clientes* → columna *Imprimir recibos* (campo `print` del negocio). Al encenderla, el dueño recibe un mensaje.
- **Mi negocio (dueño):** tarjeta *Imprimir recibos* (`print` en `tenants/{tid}/settings/opts_{tid}`). Si el dueño ya la tocó, manda lo que él eligió; si nunca la tocó, vale lo que Samanat dejó en la consola. Si Samanat la cambia después, el negocio queda como Samanat la dejó.

Encendida, cada recibo (ventas de caja, pagos de mesas y ventas anteriores en *Ventas*) trae el botón **Imprimir** y el enlace *Configurar impresora*. La impresora se configura **en cada equipo** (se guarda en el navegador, `localStorage` → `natara_printer`), porque cada caja o celular tiene la suya:

- **Impresora del equipo** (por defecto): abre la ventana de impresión con el recibo ajustado al papel. Sirve para térmicas USB o de red instaladas en el computador, impresoras Wi-Fi, Bluetooth emparejadas con el celular y cualquier impresora normal.
- **Térmica Bluetooth directo** (Chrome o Edge en Android, Windows y Mac; no en iPhone): toca *Buscar impresora*, se conecta por Web Bluetooth y el recibo sale sin ventana de impresión, con comandos ESC/POS (sin tildes, para que no salgan símbolos raros) y corte de papel si la impresora tiene cortador. Se reconecta sola a la última impresora. Las impresoras solo Bluetooth clásico no aparecen: se emparejan en el celular con una app de servicio de impresión (por ejemplo RawBT) y se usa *Impresora del equipo*.
- **Papel:** térmica 58 mm (32 letras), térmica 80 mm (48 letras) o carta / media carta.
- **Copias** (1 a 3) e **Imprimir solo al terminar cada venta** (si está apagado, se imprime con el botón cuando el cliente lo pida).
- *Imprimir prueba* saca un recibo de ejemplo con los datos del negocio.
- No hay que cambiar las reglas de Firebase.

## Caja por categorías

Opción **sin costo** en cualquier plan. El dueño la enciende o apaga en *Mi negocio* (Samanat también puede dejarla encendida desde la consola). Apagada, la caja sigue igual que siempre.

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

## Visitas a la demo
- La demo pública (`/demo/`) cuenta sus visitas en Firestore, colección `demovisits`: un documento `total` y uno por día (`d_AAAA-MM-DD`, hora de Colombia).
- **Personas** = navegadores distintos (se marca con `localStorage`). **Visitas** = veces que abrieron la demo (una por pestaña o sesión).
- No cuentan la app real, la consola de demo ni las vistas previas fuera de la demo publicada.
- En la demo, el aviso "X personas han probado Natara" aparece desde `VIS_MIN` (10) personas. En la consola (Resumen) se ven los totales, hoy, los últimos 7 días y una gráfica de 14 días.
- **Reglas:** se agregó `demovisits` (lectura pública; cada escritura solo suma 1 visita y máximo 1 persona). Hay que volver a pegar `firestore.rules` en Firebase.

## Impuestos en el recibo

En *Mi negocio → Régimen* el dueño elige **No responsable de IVA**, **Responsable de IVA** o **Responsable de impuesto al consumo** (restaurantes y bares, INC 8%). Los precios siempre incluyen el impuesto; si el negocio es responsable, el recibo muestra *Subtotal sin IVA/impuesto*, el impuesto por tarifa y el *TOTAL*. Cada producto tiene su tarifa (IVA 19%, 5%, exento, excluido; o INC 8% / no aplica) en Inventario → editar; por defecto 19% (IVA) u 8% (INC). La venta guarda la tarifa de cada producto (`items[].tx`, `sale.tax`) para que el recibo no cambie si después se edita el producto. Con descuento por puntos el impuesto se calcula sobre lo que realmente se pagó.
