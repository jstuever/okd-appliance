#!/bin/sh
if [ ! -f "localconfig" ]; then echo "localconfig: file not found"; exit; fi
source ./localconfig

if [ -z "$CLUSTER_NAME" ]; then echo "CLUSTER_NAME undefined"; exit; fi

gcloud -q deployment-manager deployments delete ${CLUSTER_NAME}-builder
