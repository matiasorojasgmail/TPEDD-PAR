# TPEDD-PAR
El Trabajo Practico se realizo utilizando los siguientes sistemas
LDME_terciario, python3,, virtualenvwrapper, flask, bootstrap, flask-wtf, flask_script.

0. FLUJO DEL PROGRAMA
Al ingresar a la web, en la NavBar, podras iniciar sesion para poder realizar consultas, en caso que sea la primera vez que ingrese podras registrarse. Al validar usuario y contraseña, se rediccionara a Validar la Base de Datos, una vez aprobada la base seras redireccionado al Panel de Consultas, donde podras realizar consultas en la base de datos seleccionando segun necesidad.

1. EXTRUCTURA
  1.1 MODULOS UTILIZADOS
  1.2 CLASES GENERADAS  
    1.2.1: Mi_Login: Generada para que Iniciar sesion.
    1.2.2: Registro: Generada para registrase como usuarios.
    1.2.3: Cliente_Productos: Generada para CONSULTAS, que el usuario ingrese un cliente y le liste los productos que compro el             cliente ingresado.
    1.2.4: Producto_Cliente: Generada para CONSULTAS, que el usuario ingrese un producto y le liste los clientes que compraron dicho producto.
    1.2.5: Validar_Csv: Generada para validar archivo CSV


2. Al ingresar a la web, en la NavBar encontrara las siguientes opciones: 
  2.1 Ingresar: Podra iniciar sesion ingresando usuario y contraseña.
  2.2 Cerrar Sesion: Podra finalizar sesion.
  2.3 Registrase: Podra generar datos de acceso al sitio web para validar base de datos y realizar consultas.
  2.4 Panel de Consultas: Podra realizar consultas seleccionando opciones
  
3. Tutorial: Al ingresar con usuario y contraseña sera direccionado a validar base de datos para continuar, esta verificara el correcto estado de la base. En caso de error en la base, informara cual es y debera contactarse con el administrador para verificarlo.
De ser aprobada redireccionara al panel de consultas. donde podra consultar las siguientes opciones
  3.1 Buscar Por Cliente: Debera ingresar un cliente y al buscar listara los productos que compro.
  3.2 Buscar Por Productos: Debera ingresar un producto y al buscar listara los clientes que lo compraron.
  3.3 Productos Mas Vendidos: Listara los productos mas vendidos 
  3.4 Mejores Clientes: Donde Listara los mejores clientes
  3.5 Ventas: Listara las ventas

