def GenerateConfig(context):

    resources = [{
        'name': context.properties['name'] + '-builder-public-ip',
        'type': 'compute.v1.address',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': context.properties['name'] + '-builder',
        'type': 'compute.v1.instance',
        'properties': {
            'disks': [{
                'autoDelete': True,
                'boot': True,
                'initializeParams': {
                    'diskSizeGb': context.properties['root_volume_size'],
                    'sourceImage': context.properties['image']
                }
            }],
            'machineType': 'zones/' + context.properties['zone'] + '/machineTypes/' + context.properties['machine_type'],
            'networkInterfaces': [{
                'subnetwork': context.properties['subnet'],
                'accessConfigs': [{
                    'natIP': '$(ref.' + context.properties['name'] + '-builder-public-ip.address)'
                }]
            }],
            'tags': {
                'items': [
                    context.properties['name'] + '-builder'
                ]
            },
            'zone': context.properties['zone']
        }
    }, {
        'name': context.properties['name'] + '-builder-firewall',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': context.properties['network'],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': ['22']
            }],
            'sourceRanges': ['0.0.0.0/0'],
            'targetTags': [context.properties['name'] + '-builder']
        }
    }]

    return {'resources': resources}
