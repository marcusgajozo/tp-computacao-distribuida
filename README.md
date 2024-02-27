## Trabalho pratico de computação distribuida

O trabalho visa realizar uma comunicação usando protocolo UDP entre cliente e servidor.

**Cliente:**  
Contruido com um laço para forçar o servidor, simulando várias requisições de lugares diferentes.

**Servidor:**  
Contruido usando fila e threads para paralelizar as multiplas requisições, foi usando um lock para gerenciar área critica do código e vitando a inconsistência de dados.