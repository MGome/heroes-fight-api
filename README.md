# Pelea de personajes
### by Mario Gómez - { bigMario } :ghost:
## Setup inicial :rocket:
1) Las requests son realizadas por medio de la libería `requests`. En caso de ser necesario, debe ser instalada por medio del comando:
```
pip install requests
```
2) El manejo de las credenciales para el mailer es a través de `dotenv`. Este, en caso de ser necesario, debe ser instalado por medio de:
```
pip install python-dotenv 
```
3) El envío de mails se realiza a través de `smtp` (el detalle de esto está en la sección [Mailer](#mailer)). Esto puede ocasionar un error de `SSLCertVerificationError` (de acuerdo a diversas fuentes es exclusivo de Mac), el cual puede ser solucionado con cualquiera de las siguientes opciones:
- Opción 1 (exclusiva Mac, testeada): Ir desde Finder a Aplicaciones, entrar a la carpeta Python X (donde X es la versión instalada) y abrir el archivo `Install Certificates.command`. Este se encargará de ejecutar el comando que instala el certificado.
- Opción 2 (universal, no testeada): Ejecutar desde la terminal / cmd el siguiente comando:
```
pip install certifi
```

## Consideraciones generales del flujo
El sistema de combates es de 5 vs 5, donde el formato de peleas es igual al que se presenta en juegos como Mortal Kombat además de algunas consideraciones adicionales, las cuales son:
- Las batallas se juegan por rondas, donde gana el mejor de 3.
- Los personajes se enfrentan 1 vs 1, donde el que pierde es eliminado del combate en la ronda actual.
- Los enfrentamientos son decididos de forma aleatoria, donde la selección de cualquier personaje es equiprobable.
- Los ataques son por turnos, donde el que ataca primero es el que tenga una estadística de velocidad mayor.
- El personaje que gana el combate puede luchar inmediatamente en el siguiente turno con el mismo HP que terminó su combate.
- Al finalizar una ronda todos los miembros de los equipos recuperan el estado de su HP inicial.

## Supuestos
- Si bien un personaje puede ser héroe o villano, la clase que engloba ambos recibe el nombre Héroe.
- El HP y la potencia de los ataques son calculados una vez que ya se calcularon las estadísticas reales. En este caso cabe mencionar que cuando se realiza la simulación habiendo calculado el HP y la potencia de los ataques antes de calcular las estadísticas reales la simulación dura un poco más, ya que los ataques no son tan poderosos como en el caso descrito en el supuesto. Sin embargo, dado que se calculan las estadísticas reales, se consideró que hacía más sentido utilizar los nuevos valores para los cálculos (en otro caso jamás habrían sido utilizados en la simulación, sin contar la velocidad).
- El FB se calcula con la función dada para cada uno de los personajes.


## Mailer
Debido a que `mailgun` tiene una limitación de máximo 5 usuarios registrados, donde cada usuario registrado debe aceptar una invitación previamente para poder recibir mails, se decidió utilizar un método alternativo para enviar mails.

El servicio de envío de mails está configurado con el sender `manaxo.gomez@gmail.com` (mail propio), mientras que el receptor se puede asignar manualmente al finalizar la simulación.