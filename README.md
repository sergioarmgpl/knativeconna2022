# knativeconna2022
KnativeConNA Demo, using Knative at the edge
## Installing this demo

## 
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-crds.yaml

kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-core.yaml


kubectl apply -f https://github.com/knative/net-contour/releases/download/knative-v1.2.0/contour.yaml

kubectl apply -f https://github.com/knative/net-contour/releases/download/knative-v1.2.0/net-contour.yaml

kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"contour.ingress.networking.knative.dev"}}'

EXTERNAL_IP="$(kubectl get svc envoy -n contour-external  -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')"

KNATIVE_DOMAIN="$EXTERNAL_IP.nip.io" 

kubectl patch configmap/config-domain \
--namespace knative-serving \
--type merge \
--patch '{"data":{"'$KNATIVE_DOMAIN'":""}}'

kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-hpa.yaml 


kn service create api \
--image sergioarmgpl/app2demo \
--port 5000 \
--env MESSAGE="Knative demo v1" \
--revision-name=v1 --cluster-local

curl http://api.default.$EXTERNAL_IP.nip.io




[Unit]
After=network.target

[Service]
ExecStart=/usr/local/bin/disk-space-check.sh

[Install]
WantedBy=default.target