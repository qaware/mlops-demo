pipeline_version = '2.0.5'

k8s_yaml(kustomize('./kubeflow/kustomize/cluster-scoped-resources'))
k8s_yaml(kustomize('./kubeflow/kustomize/env/platform-agnostic'))

k8s_resource(workload='ml-pipeline-ui',port_forwards='7080:3000')

docker_build(
    'mlops-demo-backend',
    './backend',
    live_update=[
        sync('backend/components', '/app/components'),
        sync('backend/app.py', '/app/app.py'),
        sync('backend/pipeline.py', '/app/pipeline.py'),
        run('cd /app && pip install -r requirements.txt',
            trigger='./backend/requirements.txt')
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