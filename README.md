# Natara · by Samanat

Software de gestión para pequeños negocios (panaderías, farmacias, minimercados, papelerías): inventario, caja, ingresos y egresos, estadísticas y una consola de administración para Samanat.

## Demo

Demo en línea: https://samanat2026.github.io/natara/

`index.html` es la demo completa en un solo archivo. También se abre con doble clic en el navegador, sin servidor.

Los datos de la demo se guardan en el navegador (`localStorage`) y se sincronizan entre pestañas del mismo navegador.

### Cuentas de ejemplo

| Cuenta | Rol | Qué ve |
|---|---|---|
| Natalia Orozco | Superadmin (Samanat) | Clientes, planes, solicitudes, mensajes, bloqueo de acceso |
| Marta Gómez | Dueña · Panadería La Espiga | Todos los módulos del plan Total, sin lector |
| Juan Pérez / Laura Ríos | Cajeros · Panadería La Espiga | Caja, ventas, inventario (sin costos), fiados |
| Carlos Mejía | Dueño · Droguería Vida Sana | Plan Pro + lector de código de barras |
| Francisco Úsuga | Dueño · Minimercado Don Pacho | Cuenta suspendida (pantalla de bloqueo) |
| Andrea Vélez | Dueña · Papelería Arcoíris | Plan Pro |

## Módulos

| Módulo | Precio suelto (COP/mes) | Básico | Pro | Total |
|---|---|:-:|:-:|:-:|
| Inventario | 25.000 | ✓ | ✓ | ✓ |
| Caja y ventas (incluye apertura y cierre) | 25.000 | ✓ | ✓ | ✓ |
| Ingresos y egresos | 20.000 | | ✓ | ✓ |
| Estadísticas | 20.000 | | ✓ | ✓ |
| Empleados | 15.000 | | ✓ | ✓ |
| Fiados y clientes | 18.000 | | | ✓ |
| Proveedores | 15.000 | | | ✓ |
| Lector de código de barras (complemento) | 12.000 | | | |

Planes: Básico $49.900 · Pro $89.900 · Total $129.900 al mes.

## Próximos pasos

- Versión de producción en Angular + Firebase (Auth, Firestore, Hosting) con datos reales por negocio y bloqueo en tiempo real entre dispositivos.
- Producto 2: agendamiento de citas para salones de uñas por WhatsApp.
