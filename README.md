# E2R images API

Trabajo realizado bajo una beca de colaboración con el departamento de IA de la UPM. En este repositorio esta disponible tanto el [informe final](./documentacion/InformeFinal.pdf) como la [presentación](./documentacion/OEG_presentaci%C3%B3n_beca.pptx) dada en el departamento. La web y API estan disponibles en este [dominio](https://imagenese2r.linkeddata.es/) del OEG.

![Imagen de la web desarrollada](https://github.com/DavidCanoRosillo/E2R_images_API/blob/master/documentacion/web.png)

## Descripción del trabajo
Consiste en la automatización de 3 pautas de la metodología Easy2Read. Esta metodologia propone una serie de pautas para facilitar la lectura de documentos a peronas con discapacidades intelectuales. Las 3 pautas automatizadas usando el estado del arte en deep learning son:

- Titular las imágenes.
- Evitar diagramas, gráficos estadísticos y tablas técnicas.
- Utilizar imágenes de apoyo al texto, que hagan referencia al mismo explícitamente y con un vínculo claro.

La API y web desarrollada tiene las siguientes funcionalidades para cada pauta:

-	Generar descripciones automáticamente en base a una imagen.
-	Detectar imágenes con distintos tipos de gráficos para eliminarlas del documento.
-	Detectar cuando un texto no referencia explícitamente una imagen.

## Datasets usados 

Para la segunda pauta se hizo finetuning de un clasificador de imagenes. Se puede consultar en entrenamiento y dataset en el siguiente cuaderno de [kaggle](https://www.kaggle.com/code/davidcanorosillo/graph-classification).

Para la tercera pauta se hicieron extensas pruebas descritas en el informe final. El dataset usado consiste en noticias y sus imagenes. Es el subconjunto de noticias en español con imagenes descargables del dataset Latest News de esta [página](https://newsdata.io/datasets). El dataset limpiado esta disponible en mi [Google Drive](https://drive.google.com/file/d/1iLEPBoCtwXSeI4VKFp7mcD4Xx97NIDBu/view?usp=sharing). 

## Despliegue usando Docker
Este repositorio contiene un archivo Dockerfile para hacer más cómodo el despliegue. Ejecutando estos comandos se puede ejecutar la API.

```
    docker build -t E2R_API .

    docker run -p <puerto-host>:80 E2R_API
```
Reemplazando \<puerto-host> con el puerto en el cual se desea exponer la API.