# Docker Stacks

Un stack es un grupo de servicios interrelacionados que comparten dependencias, y que pueden ser orquestados y escalados. Un simple stack es capaz de definir y coordinar la funcionalidad de una aplicación. (Aplicaciones más complejas pueden usar múltiples stacks).

## Nuestro primer Stack

La manera de definir stacks es con un archivo llamado `hello-service.yml`. Este archivo define como se debería comportar el stack en producción. 

```YAML
version: "3.3"
services:
  # Solo tenemos un servicio que llamaremos "web"
  web:
    # El nombre de la imagen que creamos en la anterior sección
    image: hello-docker
    # En esta parte definimos la estrategia para correr los contenedores.
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
      restart_policy:
        condition: on-failure
    ports:
      - "80:80"
    networks:
      - webnet

networks:
  webnet:
```

Este archivo le indica a `Docker` que haga lo siguiente:

* Usar la imagen que creamos en la sección anterior 
* Correr tres instancias de esa imagen en un servicio llamado web, limitando a cada uno usar como máximo el 10% del CPU, y 50 MB de RAM
* Reiniciar los contenedores inmediatamente si uno falla.
* Asignar el puerto 80 del host al puerto 80 del servicio.
* Instruir a los contenedores compartir el puerto 80 a través de la network llamada webnet
* Definimos la network webnet con los valores por defecto

Ahora levantemos el stack. Corriendo el siguiente comando:

```
$ docker stack deploy -c hello-service.yml hello-service
```

Nuestro servicio está corriendo tres instancias de contenedores de nuestra imagen en un host.

Ahora podemos correr `curl http://localhost` muchas veces, o ir a esa URL en un navegador y recargar la página.
Verás que el ID del contenedor cambia, es el load-balancer en acción; en cada solicitud, una de las 5 réplicas es elegída, en round-robin, para responder.

Magic ✨🐳

Bueno ahora borremos el **stack**

```
$ docker stack rm hello-service
```

## Stacks multi-servicios

Ahora hagamos algo real y deployemos un stack de mas de un servicio.

Vamos agregar a el servicio `hello-docker` un visualizador y un `redis` para persistir los datos. Ahora podremos contabilizar los visitantes de nuestro servicio ;-)

En esta carpeta encontrarás el archivo `hello-stack.yml` con el siguiente contenido:

```YAML
version: "3"
services:
  web:
    image: hello-docker
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
    ports:
      - "80:80"
    networks:
      - webnet
  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
  redis:
    image: redis
    ports:
      - "6379:6379"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
networks:
  webnet:
```

Como puedes ver, agregamos dos servicios`redis` y `visualizer`, cada uno con sus politicas y constraints.

Levantemos el stack y veamos que pasa:

```
$ docker stack deploy -c hello-stack.yml hello
```

Magic ✨🐳

Magic ✨🐳

Magic ✨🐳

```
$ docker service ls
```

Verás algo como esto:
```
ID                  NAME                MODE                REPLICAS            IMAGE                             PORTS
i08fo6eilog8        hello_redis         replicated          1/1                 redis:latest                      *:6379->6379/tcp
nch7igvp6l16        hello_visualizer    replicated          1/1                 dockersamples/visualizer:stable   *:8080->8080/tcp
px5kj7d22t8x        hello_web           replicated          3/3                 hello-docker:latest               *:80->80/tcp
```

Wujuu! Ahora tenemos un `stack` con tres servicios! El servicio `web` con 3 instancias corriendo y su carga es balanceada automáticamente por docker, el servicio `redis` que persiste los datos de los visitantes del sitio y el servicio `visualizer` para ver como los servicios están deployados.

> :shipit: Ahora puedes **visualizar** los servicios deployados conectándote al servicio `visualizer` yendo a [localhost:8080] 

> :shipit: Intentá correr el siguiente commando para chequear como la carga del servicio web es balanceada y como el historial de visitas es persistido.

```
$ while sleep 1; do curl localhost && echo ""; done
```

Ahora, escalemos el servicio web con el siguiente comando:

```
$ docker service scale hello_web=5
```

Ahora paremos algunos contenedores y veamos que pasa ✨
```
$ docker stop [container id | name]
```

Para borrar el stack ejecuta el siguiente comando:
```
docker stack rm hello
```

Ahora nos ponemos más serios, vamos a distribuir nuestra aplicación en multiples nodos con [docker swarm](https://github.com/fredomartinez/hello-docker/tree/master/5-docker-swarm).