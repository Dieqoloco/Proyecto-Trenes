# Proyecto-Trenes

## Descripción
La Empresa de Ferrocarriles del Estado de Chile está realizando una importante inversión para mejorar su sistema de transporte. Entre los planes se incluyen nuevas rutas y trenes con distintas características, lo que hace necesario contar con una herramienta que permita planificar y analizar su funcionamiento.
Por esto, la División de Desarrollo Informático busca crear un Sistema de Simulación de Tráfico Ferroviario, por ello creamos una propuesta que consiste en desarrollar una aplicación que permita a los usuarios visualizar y crear simulaciones de trenes, incorporando elementos como estaciones, rutas, velocidades y capacidad de pasajeros. El sistema será modular y podrá ampliarse con nuevas funciones en el futuro, ayudando a mejorar la eficiencia y la toma de decisiones dentro de EFE.

[URl][https://github.com/Dieqoloco/INFO081-11-ProyectoTrenes.git]

## Integrantes
* Diego Alvarado
* Diego Fernández
* Emilia Barahona
* Angela Carrillo
* Daniel Muñoz

## Descripción de los indicadores

Como simulación escogimos dos indicadores los cuales son: 
-Estación más cercana: Indica cuál es la estación que se encuentra a menor distancia dentro del sistema. Sirve para identificar conexiones rápidas entre estaciones y facilitar la planificación de rutas.
-Mayor cantidad de pasajeros: Muestra cuál estación o tren tiene más personas transportadas. Este indicador ayuda a entender dónde hay más movimiento de usuarios y a mejorar la organización del servicio.

## Descripcion de la persistencia de datos

Existen 2 situaciones de escrituras y lectura de datos, la lectura estática, en la que se incluyen los archivos necesarios para iniciar la simulación que se guardaran en archivos CSV para el acceso detallado, mientras que los archivos dinámicos que son los que se actualizan durante la simulación se guardaran en archivos txt, todos los archivos se guardaran en una carpeta, se guardaran por archivos cada uno con su respectivo uso ej: estaciones.csv; eventos.txt; etc. 

## Como empezar

* 1.- crear una carpeta donde guardar el repositorio
* 2.- posicionarse dentro de esa carpeta en el terminal **cd mi_carpeta**
* 3.- escribir git clone https://github.com/Dieqoloco/INFO081-11-ProyectoTrenes.git
* 4.- escribir cd INFO081-11-ProyectoTrenes
* 5.- escribir python programa.py