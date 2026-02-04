## Docker API

### Pull image
```bash
docker pull dyath/watt-about-it
```

### Run
```bash
docker run --env-file .env -p 8081:8000 dyath/watt-about-it:latest
```

### Interface
Se rendre sur https://<ip-machine>:8081/docs pour tester l'API