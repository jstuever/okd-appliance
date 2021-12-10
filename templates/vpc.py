def GenerateConfig(context):

    resources = [{
        'name': context.properties['cluster_name'] + '-network',
        'type': 'compute.v1.network',
        'properties': {
            'region': context.properties['cluster_region'],
            'autoCreateSubnetworks': False
        }
    }, {
        'name': context.properties['cluster_name'] + '-subnet',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': context.properties['cluster_region'],
            'network': '$(ref.' + context.properties['cluster_name'] + '-network.selfLink)',
            'ipCidrRange': context.properties['cluster_cidr']
        }
    }, {
        'name': context.properties['cluster_name'] + '-router',
        'type': 'compute.v1.router',
        'properties': {
            'region': context.properties['cluster_region'],
            'network': '$(ref.' + context.properties['cluster_name'] + '-network.selfLink)',
            'nats': [{
                'name': context.properties['cluster_name'] + '-nat',
                'natIpAllocateOption': 'AUTO_ONLY',
                'minPortsPerVm': 7168,
                'sourceSubnetworkIpRangesToNat': 'LIST_OF_SUBNETWORKS',
                'subnetworks': [{
                    'name': '$(ref.' + context.properties['cluster_name'] + '-subnet.selfLink)',
                    'sourceIpRangesToNat': ['ALL_IP_RANGES']
                }]
            }]
        }
    }, {
        'name': context.properties['cluster_name'] + '-internal',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.' + context.properties['cluster_name'] + '-network.selfLink)',
            'allowed': [{
                'IPProtocol': 'icmp'
            },{
                'IPProtocol': 'tcp',
                'ports': ['22']
            },{
                'IPProtocol': 'tcp',
                'ports': ['6443']
            }],
            'sourceRanges': [context.properties['cluster_cidr']]
        }
    }]

    return {'resources': resources}
