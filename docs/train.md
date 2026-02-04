## Docker entraînement

### Build
```bash
docker build -f docker/Dockerfile.train -t filrouge-train .
```

### MLFLOW
```bash
mlflow ui
```

### Run
```bash
docker run --rm \
  -v "$(pwd)/data/processed:/app/data/processed" \
  -v "$(pwd)/training/models:/app/models" \
  filrouge-train
```

### Explication des volumes
data/processed → montage des données en lecture <br>
training/models → stockage des modèles entraînés hors du conteneur