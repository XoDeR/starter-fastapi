# Tilt UI port is 10360 — do not use the default 10350 (already in use on this machine).
# Start with:
#   .\tilt-up.ps1
# or:
#   tilt up --port 10360
# UI: http://localhost:10360/

version_settings(constraint='>=0.33.0')
allow_k8s_contexts('minikube')

print('Tilt UI: http://localhost:10360/  (start with .\\tilt-up.ps1 or tilt up --port 10360)')

### K8s Config ###

k8s_yaml('./infra/development/k8s/namespace.yaml')
k8s_yaml('./infra/development/k8s/secrets.yaml')
k8s_yaml('./infra/development/k8s/app-config.yaml')
k8s_resource(
  new_name='config',
  objects=[
    'fastapi-starter:namespace',
    'postgres-credentials:secret:fastapi-starter',
    'app-config:configmap:fastapi-starter',
  ],
  labels='tooling',
)

### End of K8s Config ###

### Postgres ###

k8s_yaml('./infra/development/k8s/postgres-deployment.yaml')
k8s_resource(
  'postgres',
  port_forwards=['5432:5432'],
  resource_deps=['config'],
  labels='tooling',
)

### End Postgres ###

### starter-api ###

docker_build(
  'fastapi-starter/starter-api',
  '.',
  dockerfile='./infra/development/docker/starter-api.Dockerfile',
  only=['./starter-api'],
  live_update=[
    sync('./starter-api', '/app'),
  ],
)

k8s_yaml('./infra/development/k8s/starter-api-deployment.yaml')
k8s_resource(
  'starter-api',
  port_forwards=['8000:8000'],
  resource_deps=['postgres'],
  labels='services',
)

### End of starter-api ###

### Web Frontend ###

docker_build(
  'fastapi-starter/web',
  '.',
  dockerfile='./infra/development/docker/web.Dockerfile',
  only=['./web'],
  live_update=[
    sync('./web', '/app'),
  ],
)

k8s_yaml('./infra/development/k8s/web-deployment.yaml')
k8s_resource(
  'web',
  port_forwards=['5173:5173'],
  resource_deps=['starter-api'],
  labels='frontend',
)

### End of Web Frontend ###
