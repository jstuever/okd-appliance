#!/bin/sh
if [ ! -f "localconfig" ]; then echo "localconfig: file not found"; exit; fi
source ./localconfig

if [ -z "$BUILDER_IMAGE" ]; then echo "BUILDER_IMAGE undefined"; exit; fi
if [ -z "$CLUSTER_NAME" ]; then echo "CLUSTER_NAME undefined"; exit; fi
if [ -z "$CLUSTER_REGION" ]; then echo "CLUSTER_REGION undefined"; exit; fi

export CLUSTER_NETWORK=$(gcloud compute networks describe ${CLUSTER_NAME}-network --format json | jq -r .selfLink)
export CLUSTER_SUBNET=$(gcloud compute networks subnets describe ${CLUSTER_NAME}-subnet --region=${CLUSTER_REGION} --format json | jq -r .selfLink)
export CLUSTER_ZONE_0=$(gcloud compute regions describe ${CLUSTER_REGION} --format=json | jq -r .zones[0] | cut -d "/" -f9)

if [ -z "$CLUSTER_NETWORK" ]; then echo "CLUSTER_NETWORK undefined"; exit; fi
if [ -z "$CLUSTER_SUBNET" ]; then echo "CLUSTER_SUBNET undefined"; exit; fi
if [ -z "$CLUSTER_ZONE_0" ]; then echo "CLUSTER_ZONE_0 undefined"; exit; fi

if [ ! -d "assets" ]; then mkdir assets; fi
if [ ! -L "assets/templates" ]; then ln -s ../templates assets; fi

## Launch builder instance
cat <<EOF >assets/builder.yaml
imports:
- path: templates/builder.py
resources:
- name: cluster-builder
  type: templates/builder.py
  properties:
    name: '${CLUSTER_NAME}'
    image: '${BUILDER_IMAGE}'
    network: '${CLUSTER_NETWORK}'
    machine_type: 'n1-standard-4'
    region: '${CLUSTER_REGION}'
    root_volume_size: '128'
    subnet: '${CLUSTER_SUBNET}'
    zone: '${CLUSTER_ZONE_0}'
EOF

gcloud deployment-manager deployments create ${CLUSTER_NAME}-builder --config assets/builder.yaml
