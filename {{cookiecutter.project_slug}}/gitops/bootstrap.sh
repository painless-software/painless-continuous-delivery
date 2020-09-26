#!/usr/bin/env bash

if [[ $(helm version --short 2> /dev/null | head -c 3) != 'v3.' ]]; then
    echo 'Error: Helm v3 is required to run this script. Aborting.'
    exit 1
fi

set -o errexit
set -o pipefail
set -o nounset

FLUX_NAMESPACE=fluxcd
GIT_REPO="$(git remote get-url origin)"
GIT_HOST="$(echo ${GIT_REPO} | sed -e 's#^https://##' -e 's#/.*$##' \
                                   -e 's/^git@//'     -e 's/:.*$//')"
KNOWN_HOSTS="$(ssh-keyscan ${GIT_HOST} 2> /dev/null | tail -1)"

kubectl create namespace ${FLUX_NAMESPACE} --save-config --dry-run --output yaml \
  | kubectl apply -f -

helm repo add fluxcd https://charts.fluxcd.io
helm repo update

helm install flux fluxcd/flux \
  --set git.path=namespaces,workloads \
  --set git.pollInterval=1m \
  --set git.url=${GIT_REPO} \
  --set manifestGeneration=true \
  --set sops.enabled=true \
  --set-string ssh.known_hosts="${KNOWN_HOSTS}" \
  --namespace ${FLUX_NAMESPACE}

helm install helm-operator fluxcd/helm-operator \
  --set git.ssh.secretName=flux-git-deploy \
  --set helm.versions=v3 \
  --set-string ssh.known_hosts="${KNOWN_HOSTS}" \
  --namespace ${FLUX_NAMESPACE}

if which fluxctl > /dev/null; then
    fluxctl identity --k8s-fwd-ns=${FLUX_NAMESPACE}
fi
