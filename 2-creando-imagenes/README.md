# Imágenes de Docker

En esta sección vamos a manejar, definir y construir nuestras propias imágenes.

## Descargando imagenes

Las **Imágenes** son templates que Docker utiliza para crear contenedores. Si estás familiarizado con la [Programación orientada a objetos](https://es.wikipedia.org/wiki/Programación_orientada_a_objetos) podrías pensar que las imágenes son las _clases_ y los contenedores son las _instancias_.


Veamos que imágenes tenemos en nuestro repositorio local:

```Shell
$ docker images
```

Intentemos descargar una imagen

```Shell
$ docker pull python:2.7-slim
```

Este comando _descarga_ (pull) la imagen llamada `python` con el tag "2.7-slim" desde el [repositorio público de Docker](https://hub.docker.com) a tu máquina. Esto es muy similar a `git pull` de un repositorio público `git` 

Bien! Ahora tenemos una imagen, ahora podremos crear un contenedor.


## Creando tu primer imagen

Una imagen de Docker está hecha por una o más capas (como Shrek). Cada capa está construida sobre la anterior y todas son inmutables. Esto significa que no podrás modificar una capa existente, pero podreas crear una nueva partiendo desde una capa anterior. Es muy similar a `git diff`.

Un archivo Dockerfile es un documento de texto que contiene todos los comandos necesarios para ensamblar una imagen de docker.

Para obtener el `Dockerfile` que usaremos, puedes clonar este repo:

```
$ git clone https://github.com/bitlogic/hello-docker/

``` 

En la carpeta /2-creando-imagenes encontrarás el archivo. Tendrá los siguientes comandos:

```Dockerfile
# Usamos una imagen oficial de Python como imagen padre
FROM python

# Seteamos /app como directorio de trabajo
WORKDIR /app

# Copiamos el código de nuestra aplicación y sus dependencias en /app
COPY . .

# Instalamos los paquetes expecificados en requirements.txt
RUN pip install -r requirements.txt

# Exponemos el puerto 80
EXPOSE 80

# Definimos una variable de entorno
ENV NAME Bitlogic

# Cuando corramos esta imagen, por defecto se ejecutará este comando
CMD ["python", "app.py"]
```

 Bueno ahora creemos la imagen con el siguiente comando:

```Shell
$ docker build -t hello-docker .
```

Si prestas atención al output del comando, verás que cada instrucción (`FROM`, `RUN`, etc.) en el `Dockerfile` genera un capa inmutable.

Y listo! 🐳 Ahora podemos chequear la nueva imagen con este comando:

```Shell
$ docker images
```

Ahora ejecutemos la imagen que acabamos de crear.

```
$ docker run --name hello -d -P hello-docker 
```

Vamos!!! Ahora tenemos nuestra propia app dockerizada corriendo en nuestra máquina:

Podemos chequear que la aplicación está corriendo entrando con un navegador a `localhost:[puerto]`


O también usando el comando `curl`

``` 
$ curl http://localhost:[puerto]

<h3>Hello Bitlogic!</h3><b>Hostname:</b> 8fc990912a14<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>
```



## Echemos un vistazo a las capas

Si ejecutas de nuevo el comando `docker build`, tomará mucho menos tiempo que la primera vez. Esto es porque Docker guarda en la caché cada capa y no es necesario volver a contruirlas si no ha cambiado nada desde la última vez que se creó.

Si cambiamos en nuestro Dockerfile la instrucción `FROM python:2.7-slim` a `FROM python` y creamos de nuevo la imagen, se creará con la última versión de  `python`.
Verás que todas las capas se vuelven a correr. Esto sucede porque cuando editamos una capa, se volveran a ejecutar las capas siguientes a ésta. Y como cambiamos la _capa base_, todas las siguientes se volvieron a ejecutar, invalidando la caché.

> :bulb: A la hora de definir tu Dockerfile, siempre intenta colocar las instrucciones más estables al principio. Esto mejorará el tiempo de construcción de la imagen.

Ahora podemos publicar la imagen usando el comando `docker push`, pero necesitarás una cuenta en [`hub.docker.com`](https://hub.docker.com); Esto puedes intentarlo por tu cuenta

No hay mucho más que decir sobre imágenes de Docker, ahora es tiempo de aprender a [crear servicios](https://github.com/fredomartinez/hello-docker/tree/master/3-servicios)

