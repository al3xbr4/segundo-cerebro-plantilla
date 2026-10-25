---
tipo: concepto
etiquetas: [empresa, administracion]
---

# Administración de la empresa en el cerebro

La idea: meter **toda la documentación administrativa** en una carpeta y poder preguntarle a la IA lo que sea, en cualquier momento.

- «¿Cuándo vence el seguro de la nave y con cuánto preaviso hay que avisar?»
- «¿Cuánto pagamos al mes de alquileres y licencias?»
- «¿Qué contratos renuevan solos este trimestre?»
- «¿Qué certificados u homologaciones caducan antes de fin de año?»
- «Resúmeme las condiciones del contrato con el proveedor X.»

Funciona igual para lo personal (piso, seguros, coche, impuestos) que para la empresa. Lo que cambia en la empresa son los **permisos**.

## Cómo funciona

1. Los documentos (PDF, Word, Excel, fotos) se dejan en `raw/documentos/`, o en subcarpetas por área: `raw/documentos/finanzas/`, `raw/documentos/personas/`…
2. La rutina diaria (o «procesa raw») hace a cada uno una **ficha** con su resumen y los campos administrativos: categoría, contraparte, importe, inicio, `vence`, renovación y `preaviso_dias`. Ver «Documentos administrativos» en `AGENTS.md`.
3. `scripts/vencimientos.py` rehace cada día [[wiki/Vencimientos]]: lo vencido, lo de los próximos 30 y 90 días, y la fecha límite para avisar cuando hay preaviso.
4. Cada contraparte (aseguradora, arrendador, proveedor, cliente, organismo) tiene su nota en `wiki/`, enlazada con sus documentos.

## Qué meter, por área

| Área | Documentos típicos | Sensible |
|---|---|---|
| Dirección | Escrituras, poderes, actas, contratos societarios | Sí |
| Finanzas | Seguros, préstamos, leasing, impuestos, facturas recurrentes, presupuestos | En parte |
| Operaciones | Alquileres de naves u oficinas, mantenimientos, suministros, flota | No |
| Ventas | Contratos y condiciones con clientes, ofertas firmadas | En parte |
| Personas | Contratos laborales, convenios, nóminas, formación, PRL | **Sí: solo esta área** |
| Técnica | Licencias de software, certificados, homologaciones, garantías | No |

## Personal o empresa: dónde guardarlo

- **Lo personal** va en tu bóveda personal, con su repositorio privado.
- **Lo de la empresa** debería ir en una bóveda **de la empresa**: un repositorio de una cuenta u organización de la empresa, no de una persona, para que el acceso dependa de la empresa y no de quien lo montó. Se monta igual: la misma plantilla y el mismo `SETUP.md`.
- Si varias personas la van a usar y no todas pueden ver todo (nóminas, márgenes), Obsidian no basta: quien entra a una bóveda la ve entera. Para eso está el plan de [[Cerebro De IA De Empresa]]: una bóveda o carpeta por área, con [[Matriz de permisos|matriz de permisos]], o proyectos por área en Claude Team con las fichas y la nota de vencimientos de cada área.

## Buenas prácticas

- No se copian a las fichas números de cuenta, DNI ni firmas: la ficha dice que existen y en qué documento están.
- Si un documento sustituye a otro (una póliza renovada), se mete el nuevo; la ficha del antiguo queda como historial y la IA usa el más reciente.
- Revisa la nota de vencimientos una vez por semana, o pídele a la IA: «¿qué hay urgente en vencimientos?».
- Límite práctico de unos 50 MB por archivo si la bóveda se sincroniza con GitHub.
