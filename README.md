# Proyecto de Detección de Vacas con Docker y Jenkins

## Prerequisitos
- Docker
- Docker Compose

## Instalación
Siga los siguientes pasos para configurar el entorno.

Para utilizar el codigo primero hay que construir la imagen de docker utilizando los siguientes comandos:

```bash
docker compose build
```

```bash
docker compose up
```

## Configuración

Luego para utilizar jenkins se debe ingresar a la siguiente direccion:

```bash
localhost:8080
```

Para obtener la contraseña de jenkins se debe ingresar al log de docker y buscar la contraseña de jenkins.

Una vez ingresada la contraseña se debe instalar los plugins recomendados y luego crear un usuario.

Luego se debe configurar el jenkins con el nombre del usuario y la contraseña.

Una vez configurado se debe crear un nuevo trabajo y configurar el repositorio de github.

Por ultimo debe darle a construir ahora y se ejecutara el pipeline.

Si se quiere utilizar la IA se debe ejecutar el script `main.py`.

Una ejecutado el script tiene que seleccionar una de las 3 opciones que se presentan en pantalla.

Si selecciona la opcion "Seleccionar video" se le abrira una ventana para seleccionar el video que desea analizar.

Si selecciona la opcion "Seleccionar directorio de imagenes" se le abrira una ventana para seleccionar el directorio de imagenes que desea analizar.

Ahora si selecciona la opcion "Iniciar deteccion con telegram" saldra una interfaz grafica que capturara la vaca y dara el procentaje de confianza de que es una vaca, marcandola con un cuadrado verde.

Tener en cuenta que para utilizar la opcion "Iniciar deteccion con telegram" se debe tener una camara.