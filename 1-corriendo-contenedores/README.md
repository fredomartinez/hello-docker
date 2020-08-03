# Docker Containers

## Hola mundo

La parte más importante de `Docker` son los *contenedores*. Hay mucho para decir sobre ellos, pero vamos a correr uno:

```
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Facil, ¿No? Vamos a echarle un vistazo a que acaba de pasar detrás de escena...

 1. El **Docker client** conectó al **Docker daemon**.
 2. El **Docker daemon** descargó la imagen "hello-world" de **Docker Hub**.
 3. El **Docker daemon** creó un nuevo **contenedor** de esa imagen que corrió el ejecutable
    que imprimió este texto.
 4. El **Docker daemon** envió el texto al **Docker client**, y este a tu terminal.


> Whoa!! Esto signigica que **Docker** está correctamente instalado y corriendo.

Ahora empecemos a explorar el contenedor

```
$ docker container ps
```

🤔 Nada... Agreguemos la flag `-a`

```
$ docker container ps -a
```

😀 Y ahí está! La opción **-a** lista no solo los contenedores en estado `running`, también los que han finalizado. Esto puede ser útil si quisieras examinarlos.


## Corriendo un contenedor

Ahora vamos un poco más allá. Vamos a correr un contenedor de Ubuntu:

Primero vamos a descargar la imagen de docker de Ubuntu del registro de imagenes.

```
$ docker pull ubuntu:20.10
```

🤔 Parece que está descargando algo, pero qué es?...

```
$ docker images
```

Como puedes ver, ahora tenemos una imagen de Ubuntu:14.04 en nuestra máquina y podemos crear nuestro contenedor.

```
$ docker container run -it ubuntu:20.10
```

Bien, ahora estamos adentro del contenedor! La opción `-it` indica que el contenedor se correrá en modo interactivo. (Es decir, `i` es intectactivo y `t` es para generar una pseudo interface TTY para la interacción)

¿Podrías decir que pasa si borramos algun archivo importante adentro del contenedor? (Por ejemplo: :warning: borrar el binario de "ls")

Después de hacerlo, salimos del contenedor escribiendo `exit`.


> :bulb: **Recuerda:** Lo que pasa en el contenedor, queda en el contenedor.

Te has dado cuenta que la primera vez que ejecutaste `docker run ubuntu:14.04` tomó un tiempo, pero la segunda vez fue inmediato. Lo que pasó es que Docker intentó correr la imagen `ubuntu:14.04`, pero no se encontraba localmente, por lo que se descargó de un repositorio público.

## Corriendo contenedores

Vamos a levantar una base de datos Mongo!

```
$ docker run --name db mongo
```

🤔 Pero no quiero estar ligado al output... Apretamos CTRL+C para salir y remover el contenedor.

```
$ docker rm db
```

Ahora corramos un nuevo contenedor de Mongo, pero en modo background con la flag `-d` (`detach`).

```
$ docker run --name db -d mongo
```

Ahora examinemos esta base de datos. Lo primero que tenemos que hacer entrar al contenedor con algo similar a `ssh`. Podemos _ejecutar_ un comando en modo interactivo:

```
$ docker exec -it db mongo
```

Este comando de docker, ejecuta el comando `mongo` en el contenedor `db`. Para salir apretamos CTRL+C para salir.


Si ahora ejecutamos `docker ps` veremos que el contenedor `db` todavía está corriendo. No ha parado porque el proceso principal `db` todavía sigue corriendo.
El proceso que acabamos de parar fue solo el del shell de mongo.


## Exponiendo contenedores

Ahora corramos una aplicación web en _otro_ contenedor.

```
$ docker container run --name webapp -d -P seqvence/static-site
```

La opción `-P` basicamente indica a Docker que asigne automaticamente el puerto interno que el contenedor expone a un puerto disponible en tu máquina.
Veamos si la aplicación está corriendo y a qué puerto está expuesto.


```
$ docker container ps
```

Como puedes ver en `PORTS`, parece que la app está corriendo en el puerto 80, pero... 😮 Espera! Es solo el puerto _interno_ del contenedor.

Intenta conectarte en un browser a \\localhost:{->puerto}

¡Felicitaciones! Ahora tenés una aplicación web corriendo adentro de un contenedor y siendo expuesto para que los usuarios puedan usarlo 😎 🐳.


## Docker Logs


Uno de los beneficios de Docker es que ofrece una interface estándar para operar las aplicaciones adentro de los contenedores. 
Veamos como podemos ver los logs de nuestra aplicación web adentro del contenedor.

> Nota: para poder ver los logs, la aplicación andetro del contenedor debe enviar sus logs a STDOUT y STDERR


```
$ docker logs webapp
```

## Borrando contenedores

OK, sabemos como arrancar contenedores, ahora veamos como pararlos.

Primero, veamos que contenedores están corriendo:

```
$ docker container ps
```

Ahora lo paremos de la siguiente manera:

``` 
$ docker container stop {container id | container name}
```

Genial! Este comando paró el contenedor pero todavía tenemos archivos del contenedor en el host. Si quisieras hacer una limpieza completa y borrar todos, tendrias que ejecutar el siguiente comando:

``` 
$ docker container prune
```
El comando `prune` borrará todo los contenedores que no estén corriendo. Lo podrías chequear con el comando `docker container ps -a`, verás que no hay más contenedores en tu máquina.


#### Bonus :trollface: :trollface: :trollface:

Si quisieras verte como un **hacker de Hollywood** con `Docker`, lo podrías hacer con el siguiente comando:

```
$ docker container run -it jturpin/hollywood hollywood
```
:grimacing:


Eso fue una introducción de Docker :bowtie:. Vayamos a la [siguiente sección](https://github.com/fredomartinezm/hello-docker/tree/master/2-creando-imagenes). :punch:
