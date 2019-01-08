# From Github arsaboo
# https://github.com/arsaboo/homeassistant-config
#
# Combine multiple device trackers into one entity
# You can call the script using the following:
# - service: python_script.meta_device_tracker
#   data_template:
#     entity_id: '{{trigger.entity_id}}'
# OPTIONS

people = {
    'device_tracker.mike_meta' : {
        'friendly_name' : 'Mike',
        'entity_picture': '/local/mike.jpg',
        'trackers'      : [
            'device_tracker.mike_iphone_ios',
            'device_tracker.mike_iphone'
        ]
    },
    'device_tracker.clara_meta' : {
        'friendly_name' : 'Clara',
        'entity_picture': '/local/clara.jpg',
        'trackers'      : [
            'device_tracker.clara_iphone_ios',
            'device_tracker.clara_iphone'
        ]
    },
    'device_tracker.mikey_meta' : {
        'friendly_name' : 'Mikey',
        'entity_picture': '/local/mikey.jpg',
        'trackers'      : [
            'device_tracker.mikey_iphone'
        ]
    },
    'device_tracker.bryan_meta' : {
        'friendly_name' : 'Bryan',
        'entity_picture': '/local/bryan.jpg',
        'trackers'      : [
            'device_tracker.bryan_iphone'
        ]
    },
    'device_tracker.jim_meta' : {
        'friendly_name' : 'Jim',
        'entity_picture': '/local/jim.jpg',
        'trackers'      : [
            'device_tracker.jim_phone'
        ]
    },
    'device_tracker.kasey_meta' : {
        'friendly_name' : 'Kasey',
        'entity_picture': '/local/kasey.jpg',
        'trackers'      : [
            'device_tracker.kasey_phone'
        ]
    }
}

# Get the entity that triggered the automation
triggeredEntity = data.get('entity_id')

# if the triggering entity is the meta device tracker then we need to
#   use most recent tracker for that person
# the only time this happens is when the start script calls this script
if triggeredEntity in people:
    person = people.get(triggeredEntity)
    triggeredEntity = person.get('trackers')[0]
    last_changed = hass.states.get(triggeredEntity).last_changed
    for entity in person.get('trackers'):
        state = hass.states.get(entity)
        if state != None:
            if state.last_changed > last_changed:
                triggeredEntity = entity
                last_changed = state.last_changed

# default is no matching meta entity
metaEntity = None
# find the person that matches the triggeredEntity
for key,val in people.items():
    person = people.get(key)
    if triggeredEntity in person.get('trackers'):
        # we have a match
        metaEntity = key
        newFriendlyName = person.get('friendly_name')
        newEntityPicture = person.get('entity_picture')


# do nothing if triggeredEntity is not a tracker for any of our people
if metaEntity != None:
    # Get current & new state
    newState = hass.states.get(triggeredEntity)
    currentState = hass.states.get(metaEntity)

    # Get New data
    newSource = newState.attributes.get('source_type')

    # If GPS source, set new coordinates
    if newSource == 'gps':
        newLatitude = newState.attributes.get('latitude')
        newLongitude = newState.attributes.get('longitude')
        newgpsAccuracy = newState.attributes.get('gps_accuracy')
    # If not, keep last known coordinates
    elif ((currentState is not None)
          and (currentState.attributes.get('latitude') is not None)):
        newLatitude = currentState.attributes.get('latitude')
        newLongitude = currentState.attributes.get('longitude')
        newgpsAccuracy = currentState.attributes.get('gps_accuracy')
    # Otherwise return null
    else:
        newLatitude = None
        newLongitude = None
        newgpsAccuracy = None

    # Get Battery
    if newState.attributes.get('battery') is not None:
        newBattery = newState.attributes.get('battery')
    elif ((currentState is not None)
          and (currentState.attributes.get('battery') is not None)):
        newBattery = currentState.attributes.get('battery')
    else:
        newBattery = None

    # Get velocity
    if newState.attributes.get('velocity') is not None:
        newVelocity = newState.attributes.get('velocity')
    elif ((currentState is not None)
          and (currentState.attributes.get('velocity') is not None)):
        newVelocity = currentState.attributes.get('velocity')
    else:
        newVelocity = None

    # Get State
    if newState.state is not None:
        nextState = newState.state
    else:
        nextState = currentState.state

    # Create device_tracker.meta entity
    hass.states.set(metaEntity, nextState, {
        'friendly_name': newFriendlyName,
        'entity_picture': newEntityPicture,
        'source_type': newSource,
        'battery': newBattery,
        'gps_accuracy': newgpsAccuracy,
        'latitude': newLatitude,
        'longitude': newLongitude,
        'velocity': newVelocity,
        'update_source': triggeredEntity
    })
