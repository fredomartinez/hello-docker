# Docker swarm

El modo Docker swarm te permite crear entornos de gran escala y disponibilidad. Basicamente te permite manejar las máquinas del cluster como un simple Docker 
con conmutación por error automática, programación de contenedores, enrutamiento y muchas otras cosas.

En esta última sección crearemos un cluster swarm simple y veremos sus conceptos básicos. Tenga en cuenta que comprender **docker swarm** en su totalidad está más allá del alcance de esta guía. En cualquier caso, vamos al grano, ¿de acuerdo?


## Configurar el clúster

### Conseguir algunos nodos

Para tener un docker swarm, necesitarás un cluster, para lo cual necesitará máquinas. La forma más rápida y genial es usando [`play-with-docker`](http://play-with-docker.com/) to try it online. 
También lo podrías probar localmente, pero necesitarás una [`docker-machine`](https://docs.docker.com/machine/) y [`Virtualbox`](https://www.virtualbox.org/).

La principal diferencia es cuanto tiempo te tomará tener el swarm listo. Si solo lo está probando, la opción online es probablemente la mejor opción. Si querés que tu swarm sea persistente o pruebe algunas cosas adicionales, podrás ir por el enfoque local (puede requerir muchos recursos).

Por simplicidad,  n esta sección vamos a utilizar `play-with-docker`.


Vamos a [`play-with-docker`](http://play-with-docker.com/) y cramos tres nodos con el botón "+ ADD NEW INSTANCE".


### Empezamos con el nodo master

Arranquemos el swarm. Ahora elijamos cuál será su nodo administrador y ejecutamos el siguiente comando:

```
$ docker swarm init --advertise-addr <id nodo manager>

Swarm initialized: current node (v51je0ntr6h0o92bbmvuka34o) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-03hh4r65g8urdusbqnlfeakp6fskg17frbb92kx1v86oa3mwsb-duninzcwphu4cvnzeh5vbmghe <ip-nodo-manager>:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

> Esto configura Docker en modo swarm y genera el comando `swarm join` que necesitará para que otros nodos se unan a este nodo. Cópialo en tu portapapeles; Lo necesitarás pronto.

### Agregando los workers

Ahora hagamos que los otros nodos se unan al swarm: ejecute el comando que acaba de copiar en su portapapeles dentro de cada uno. 


```
docker node ls
```

Ahora tenemos tres nodos trabajando para el cluster 😎

## Swarming

### Nuestro primer servicio swarm

Vamos a empezar creando un servicio:

```
$ docker service create --replicas 5 -p 80:80 --name web nginx:1.12
```

Ahora veamos cómo han sido programados

```
$ docker service ps web
```

### Escalando nuestro servicio


Esto se realiza a través del comando docker `service scale`. Actualmente tenemos 5 contenedores funcionando. Vamos a subirlo a 8 como se muestra a continuación ejecutando el comando en el nodo del administrador.

```
$ docker service scale web=8
web scaled to 8
```

Ahora veamos que tenemos el servicio escalado
```
$ docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE     PORTS
x7ag3q8hwxi0        web                 replicated          8/8                 nginx:1.12     *:80->80/tcp
```

Puede verificar en qué nodos se ejecutan los contenedores con el comando `docker service ps`.


### Inspeccionando los nodes


Puede inspeccionar los nodos en cualquier momento a través del comando `docker node inspect`.

Por ejemplo, si ya estás en el nodo (por ejemplo, en el manager) que desea verificar, puede usar el nombre self para el nodo.

```
$ docker node inspect --pretty self
```

Pero si quisieras verificar el estado de otros nodos, tendrás que pasarle el nombre del nodo. Por ejemplo:
```
$ docker node inspect --pretty node2
```

Otra forma útil de verificar lo que se está ejecutando en cada nodo es `docker node ps`. p.ej.:

```
$ docker node ps node2
```

### Un poco más sobre nodos

Si un nodo está ACTIVO,

Si un nodo está ACTIVO, está listo para aceptar tareas del nodo manager. Por ejemplo: Podemos ver la lista de nodos y su estado con el siguiente comando en el nodo administrador.

```
$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAG
ER STATUS
v51je0ntr6h0o92bbmvuka34o *   node1               Ready               Active              Leade
r
wpwocg35s2umag99w8wqctqgc     node2               Ready               Active
43rdiv13nznic9bm1ml5fgzwn     node3               Ready                Active
$
```


Como puedes ver, su disponibilidad (AVAILABILITY) está establecida en activo (Active). Cuando el nodo está activo, puede recibir nuevas tareas:

* durante una actualización de servicio para escalarlo
* durante una actualización continua (rolling update)
* cuando una tarea falla en otro nodo


Pero a veces, tenemos que desactivar un nodo por alguna razón de mantenimiento. Esto significaba establecer la disponibilidad en modo de drenaje. Probemos eso con uno de nuestros nodos.
Supongamos que queremos detener el nodo 2


```
$ docker node update --availability drain node2
```

Ahora compruebe cómo se ha drenado el nodo2 y se han movido todos sus contenedores a otros nodos.

```
$ docker service ps web
```


### Actualizaciones continuas (rolling updates)

Esto es sencillo. En caso de que tengas una imagen Docker actualizada para desplegar en los nodos, todo lo que necesitas hacer es activar un comando para actualizar el servicio.


```
$ docker service update --image nginx:1.13 web
```

Ahora verifiquemos el estado de la actualización continua del servicio con `docker service ps`

```
$ docker service ps web
```

### Tango Down 

OK, now lets see what happens if one of the `active` and `available` node crash or is shut down by accident.

Let's kill one of the worker nodes and see how docker re-schedules its containers: in `play-with-docker` just hit the delete button in any of the worker nodes. 

You can now check the status of your service as usual by executing the following:

```
$ docker service ps web
``` 

Magic! Containers have been respawned in other nodes (if possible) so the service keep working with minimal impact by the node being shut down. 



## Final words

These are just the docker basics, you'll learn a lot more by addressing real-life scenarios, so get hackin'

Hopefully this repo will encourage you to [do some more research on your own](https://docs.docker.com) and make docker part of your development toolkit and prod pipelines.

Please feel free to update/fix anything that you see improvable in this repo, and if you liked it spread the word.

Thanks for reading 🙇
