pipeline_version = '2.0.5'

k8s_yaml(kustomize('./kubeflow/kustomize/cluster-scoped-resources'))
k8s_yaml(kustomize('./kubeflow/kustomize/env/platform-agnostic'))

k8s_resource(workload='ml-pipeline-ui',port_forwards='7080:3000',labels=['kubeflow'])

docker_build(
    'mlops-demo-backend',
    './backend',
    live_update=[
        sync('backend/components', '/app/components'),
        sync('backend/app.py', '/app/app.py'),
        sync('backend/pipeline.py', '/app/pipeline.py')
    ]
)

k8s_yaml(kustomize('./backend/kubernetes'))

k8s_resource(workload='mlops-demo-backend',port_forwards='8080:8080', labels=['mlops-demo'])

local_resource(
    name='mlops-demo-frontend',
    serve_cmd='cd ./frontend && npm start',
    readiness_probe=probe(
        period_secs=15,
        http_get=http_get_action(port=3000)
    ),
    labels=['mlops-demo']
)

k8s_yaml(kustomize('./mlflow'))

k8s_resource(workload='mlflow-tracking-server',port_forwards='5000:5000', labels=['mlflow'])


load('ext://helm_resource', 'helm_resource', 'helm_repo')

k8s_yaml(kustomize('./mongodb'))

k8s_resource(workload='mongodb', port_forwards='27017:27017')