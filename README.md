 Ambientes virtuales con Conda

En esta actividad se trabajó con ambientes virtuales de Python usando Conda. Se creó un ambiente llamado `miambiente`, se instalaron algunos paquetes requeridos para la actividad y se realizaron pruebas utilizando un archivo `.py` y un notebook `.ipynb`.

 1. Crear el ambiente virtual

Primero se creó el ambiente virtual llamado `miambiente` utilizando Conda.

Para activarlo se utilizó:


conda activate miambiente


Para comprobar que el ambiente estaba creado y activo se utilizó:


conda env list


El resultado mostró:


base                     C:\Users\Valery\anaconda3
miambiente           *   C:\Users\Valery\anaconda3\envs\miambiente


El `*` indica que `miambiente` es el ambiente que estaba activo.

2. Instalar los paquetes

En el proyecto se utiliza e instala el archivo `requirements.txt`, que contiene los paquetes necesarios para realizar los ejercicios.

Los paquetes utilizados fueron:


numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
jupyter==1.0.0
opencv-python==4.8.0.76
pillow==10.0.0


Con el ambiente `miambiente` activo se instalaron utilizando:

powershell
pip install -r requirements.txt


3. Archivo main.py

Se creó el archivo `main.py` para comprobar que se podía ejecutar un programa de Python desde el ambiente virtual.

El programa utiliza NumPy, Pandas, Matplotlib y OpenCV. Para la prueba se generan datos aleatorios, se crea un DataFrame y se realiza un gráfico de dispersión.

El archivo se ejecuta con:

python main.py


Al ejecutarlo se muestran los resultados en la consola y se genera el gráfico.

4. Archivo ejercicio.ipynb

También se creó el archivo `ejercicio.ipynb`.

El notebook contiene las celdas desarrolladas para la actividad y se trabajó desde Visual Studio Code.

Para ejecutarlo se seleccionó el kernel:


miambiente


De esta forma, el notebook utiliza el ambiente virtual y los paquetes instalados en él.

 5. Archivo .gitignore

Se creó un archivo `.gitignore` para evitar subir al repositorio archivos que no son necesarios para el proyecto.

Por ejemplo, se ignoraron carpetas y archivos generados automáticamente por Python, Jupyter y Visual Studio Code:


__pycache__/
.ipynb_checkpoints/
.vscode/
.venv/
venv/
.env


¿Qué es .gitignore?

`.gitignore` es un archivo que le indica a Git qué archivos o carpetas debe ignorar. Esto sirve para que archivos temporales, configuraciones personales o archivos generados automáticamente no se agreguen al repositorio.

Por ejemplo, cuando Python ejecuta un programa puede crear la carpeta `__pycache__`. Esta carpeta no es necesaria para compartir el código, por lo que se incluye en `.gitignore`.

6. Uso de IA

Valoración: MEDIO

Durante la realización de esta actividad utilicé inteligencia artificial como apoyo en diferente momentos del desarrollo de esta, como la instalacion, identificaación y correción de errores.

La utilicé principalmente para entender algunos comandos de Conda y Python, solucionar problemas que aparecieron durante la configuración del ambiente y recibir orientación para organizar el `README.md` y el archivo `.gitignore`.

La valoración es MEDIO porque la IA fue utilizada como herramienta de apoyo, pero los comandos se ejecutaron directamente en mi computador y los archivos, el código y el notebook fueron realizados y comprobados durante el desarrollo de la actividad.

7. Archivos del proyecto

Los principales archivos del repositorio son:

.gitignore
README.md
Instrucciones.md
environment.yml
requirements.txt
main.py
ejercicio.ipynb


Con esta actividad pude practicar, hacer una retroalimentación acerca de los conceptos y la estructura al momento de programar. Además de la creación y utilización de ambientes virtuales y comprender mejor cómo se pueden manejar las dependencias de un proyecto de Python.
