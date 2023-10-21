# Knowledge Engineering and Extraction
Personal notes and excersises for the module Knowledge Engineering and Extraction @ FHGR Chur. Using [mdbook](https://rust-lang.github.io/mdBook/) in order to generate the documentation.

## Documentation
Documentation was generated with **mdbook**. I also automated the deployment process of the documentation so that it automatically gets pushed to the `gh-pages` branch using this awesome documentation [here](https://github.com/rust-lang/mdBook/wiki/Automated-Deployment%3A-GitHub-Actions).

The documentation is available [here](https://yhutter-dv.github.io/fhgr-ke-e/).

## Setup with Docker 
First of all make sure that Docker is actually installed and the Service is running:
```bash
sudo pacman -S docker
sudo systemctl start docker.service
```
Secondly if you want to run `docker` commands without the sudo prefix you need to add your user to the docker group (replace `$USER` with your user):
```bash
sudo usermod -aG docker $USER
```
Dont forget to logout and login again and restart the docker service.

### One Time Setup
```bash
sudo docker pull stain/jena-fuseki
```
### Running the Docker Container
```bash
sudo docker run -p 3030:3030 -e ADMIN_PASSWORD=admin stain/jena-fuseki
```

## Python Code
The code examples can be found under the `code` directory.

