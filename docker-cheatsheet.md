# Docker Cheatsheet

### Imagenes
```
docker images                                   # Lista todas las imagenes en tu máquina
docker images -a                                         # Incluye las capas intermedias
docker build -t <nombre-image>  <Path/toDockerfile>                # Contruir una imagen
docker rmi                                           # Eliminar una imagen de tu máquina       
docker rmi -f                                      # Forzar la eliminación de una imagen
```


### Contenedores

```
docker --version                            # Chequear la versión de Docker en tu máquina
docker run hello-world                                             # Correr un contenedor
docker container ps                             # Listar todos los contenedores corriendo
docker container ps -a                                    # Listar todos los contenedores
docker pull <imagen>                                               # Descargar una imagen 
docker container run -it <imagen>                 # Correr una imagen en modo interactivo
docker container run -P -d <imagen>              # -P para bindear a un puerto disponible
docker container run -P -d <imagem>                           # -d correrlo en background
docker container exec -it <nombre-contenedor | id>           # conectarse a un contenedor
docker logs <nombre-contenedor | id>                      # Ver los logs de un contenedor
docker container stop <nombre-contenedor | id >                     # Parar un contenedor
docker inspect <tarea o contenedor>              # Inspeccionar la tarea de un contenedor
docker container ls -q                               # Listar las IDs de los contenedores
```

### Servicios
```
docker stack ls                                                       # Listar los stacks
docker stack deploy -c <composefile> <nombre-stack> #Correr un archivo compose específico
docker service ls                                        # Listar los servicios corriendo
docker service ps <servicio>                  # Listar las tareas asociadas a un servicio
docker stack rm <nombre-stack>                                          # Borrar el stack
docker service logs <servicio>                              # Ver los logs de un servicio
```
