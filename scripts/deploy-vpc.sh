#!/bin/sh
if [ ! -f "localconfig" ]; then echo "localconfig: file not found"; exit; fi
source ./localconfig

if [ -z "$CLUSTER_NAME" ]; then echo "CLUSTER_NAME undefined"; exit; fi
if [ -z "$CLUSTER_REGION" ]; then echo "CLUSTER_REGION undefined"; exit; fi
if [ -z "$CLUSTER_CIDR" ]; then echo "CLUSTER_CIDR undefined"; exit; fi

if [ ! -d "assets" ]; then mkdir assets; fi
if [ ! -L "assets/templates" ]; then ln -s ../templates assets; fi

## Create the VPC
cat <<EOF >assets/vpc.yaml
imports:
- path: templates/vpc.py
resources:
- name: cluster-vpc
  type: templates/vpc.py
  properties:
    name: '${CLUSTER_NAME}'
    region: '${CLUSTER_REGION}'
    cidr: '${CLUSTER_CIDR}'
EOF

gcloud deployment-manager deployments create ${CLUSTER_NAME}-vpc --config assets/vpc.yaml
