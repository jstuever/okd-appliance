def GenerateConfig(context):

    resources = [{
        'name': context.properties['name'] + '-network',
        'type': 'compute.v1.network',
        'properties': {
            'region': context.properties['region'],
            'autoCreateSubnetworks': False
        }
    }, {
        'name': context.properties['name'] + '-subnet',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': context.properties['region'],
            'network': '$(ref.' + context.properties['name'] + '-network.selfLink)',
            'ipCidrRange': context.properties['cidr']
        }
    }, {
        'name': context.properties['name'] + '-router',
        'type': 'compute.v1.router',
        'properties': {
            'region': context.properties['region'],
            'network': '$(ref.' + context.properties['name'] + '-network.selfLink)',
            'nats': [{
                'name': context.properties['name'] + '-nat',
                'natIpAllocateOption': 'AUTO_ONLY',
                'minPortsPerVm': 7168,
                'sourceSubnetworkIpRangesToNat': 'LIST_OF_SUBNETWORKS',
                'subnetworks': [{
                    'name': '$(ref.' + context.properties['name'] + '-subnet.selfLink)',
                    'sourceIpRangesToNat': ['ALL_IP_RANGES']
                }]
            }]
        }
    }, {
        'name': context.properties['name'] + '-internal',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.' + context.properties['name'] + '-network.selfLink)',
            'allowed': [{
                'IPProtocol': 'icmp'
            },{
                'IPProtocol': 'tcp',
                'ports': ['22']
            },{
                'IPProtocol': 'tcp',
                'ports': ['6443']
            }],
            'sourceRanges': [context.properties['cidr']]
        }
    }]

    return {'resources': resources}
