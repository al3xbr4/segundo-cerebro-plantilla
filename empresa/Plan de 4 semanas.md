---
tipo: proyecto
etiquetas: [empresa, plan]
creado: 2026-10-25
fuentes: []
---

# Plan de 4 semanas — cerebro de IA de empresa

Concepto: [[wiki/Cerebro De IA De Empresa]] · Primero decide tu camino: [[Elegir camino]]

## Antes de empezar: reunir
- [ ] Cada persona con su área y a quién reporta (organigrama)
- [ ] Qué información es delicada y quién puede verla
- [ ] Dónde vive cada documento (Drive, Notion, correo, PCs)
- [ ] Qué software usa cada área
- [ ] Procedimientos que se repiten

## Semana 1 · Matriz de permisos y orden de documentos
**Quién:** dueño + responsable de cada área
- [ ] Rellenar [[Matriz de permisos]]
- [ ] Crear una unidad compartida (Drive) o espacio (Notion) por área, con solo el grupo de esa área
- [ ] Mover cada documento a una sola área (si otra lo necesita, se comparte, no se copia)
- **Listo cuando:** cada documento sensible está en una sola área y su unidad tiene solo a quien dice la matriz.

## Semana 2 · La IA de cada persona
**Quién:** el dueño arma los proyectos; cada persona completa su ficha
- [ ] Crear la organización en Claude Team e invitar a cada persona
- [ ] Apagar en la configuración que se compartan proyectos con toda la organización
- [ ] Un proyecto por área con sus documentos e instrucciones → [[Plantilla - Instrucciones de area]]
- [ ] Cada persona carga su ficha en la memoria de Claude → [[Plantilla - Ficha de persona]]
- **Listo cuando:** dos cuentas de áreas distintas no ven el proyecto de la otra.

## Semana 3 · Software y procedimientos
**Quién:** el dueño habilita; cada persona conecta su cuenta
- [ ] Habilitar conectores (Drive, Gmail, Calendar…) para la organización
- [ ] Dejar en solo lectura los que no deben escribir
- [ ] Cada persona conecta su cuenta
- [ ] Subir 2–3 skills con procedimientos comunes
- [ ] Anotar en la matriz qué software usa cada área
- **Listo cuando:** desde una cuenta de ventas, la IA no encuentra un documento de RR. HH.

## Semana 4 · Piloto y subagentes
**Quién:** responsable del área piloto; el dueño revisa
- [ ] Un área usa su parte del cerebro una semana real
- [ ] Registrar en [[Registro del piloto]] cada pregunta sin respuesta y cada fuga
- [ ] Decidir subagentes necesarios → ejemplos en `empresa/subagentes/`
- **Listo cuando:** una semana sin respuestas con información de otra área.

## Métricas (revisar cada mes)
- Preguntas respondidas sin repetir contexto
- Fugas de información entre áreas → **debe ser 0**
- Preguntas sin respuesta por área (indican documentos que faltan)
- Personas que la usan cada semana, por área

## Riesgos
| Riesgo | Mitigación |
|---|---|
| Documento sensible en área equivocada | Matriz + prueba con dos cuentas |
| Proyecto compartido con toda la org | Apagar esa opción |
| Conector que escribe donde solo debería leer | Solo lectura |
| Alguien se va y sigue con acceso | Baja manual el mismo día (Team) |
| Mismo documento en dos áreas | Vive en una, se comparte |
| Información vieja | Revisión mensual por área |
