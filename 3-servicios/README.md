# Servicios de Docker

## ¿Qué son los servicios?

En una aplicación distribuida, diferentes piezas de la app son llamadas "servicios". Por ejemplo, imagínate un sitio en donde se comparten videos. Probablemente incluya un servicio para guardar los datos de la aplicación en una base de datos, un servicio para reproducir los videos, un servicio para el front-end, y más.

Los servicios son ”contenedores en producción”. Un servicio corre solo una imagen, pero codifica la forma en la que esa imagen: que puerto usar, cuántas réplicas del contenedor debe correr para que el servicio tenga la capacidad que necesite.

Al escalar un servicio cambia el número de las instancias del contenedor corriendo esa pieza de software, asignando más recursos a los servicios en el proceso.

Por suerte esto es más fácil de definir, correr y escalar servicios con la plataforma de Docker.


## Modo swarm 

Para poder deployar servicios necesitamos inicializar un `cluster swarm`. Para hacer esto, ejecuta el siguiente comando:


```
docker swarm init
```

Podes chequear que el cluster se inizializó con este comando:

```
docker node ls
```

Este cluster es de un solo nodo, el docker host será el manager del cluster. En las siguientes secciones veremos como crear cluster multi-nodos más complejos.

## Creando tu primer servicio

En esta parte vamos a crear servicios desde la linea de comandos. Pero en el mundo real, es muy común definir servicios en un archivo `docker-compose.yml`. Lo veremos en la siguiente sección.

Ok, ahora para empezar veamos si hay algún servicio corriendo.

```
docker service ls
```

Ahora, empecemos creando nuestro primer servicio. Vamos a crear un servicio con la imagen que creamos en la anterior sección

```
docker service create --name pinger --replicas=1 alpine ping docker.com
```

Veamos algo de información sobre lo que el servicio está haciendo

```
docker service inspect --pretty pinger
```

Para chequear el estado de los contenedores corriendo podemos ejecutar el siguiente comando:

```
docker service ps pinger
```

Puedes ver en que nodo está corriendo. Ahora escalemos el servicio aumentando el número de réplicas (cada réplica es un contenedor)

```
docker service scale pinger=5

docker service ls
```

;-) Cool! Ahora tenemos 5 replicas del servicio!

Ahora veamos los **logs** de todas las instancias del servicio

```
docker service logs -f pinger
```

En esta sección creamos servicios usando el comando `docker service`. En la siguiente sección nos ponemos más serios y usaremos el archivo `docker-compose.yml` para [crear un stack](https://github.com/fredomartinez/hello-docker/tree/master/4-docker-stacks).

