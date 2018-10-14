# From Github arsaboo
# https://github.com/arsaboo/homeassistant-config
#
# Combine multiple device trackers into one entity
# You can call the script using the following:
# - service: python_script.meta_device_tracker
#   data_template:
#     entity_id: '{{trigger.entity_id}}'
# OPTIONS
# List the trackers for each individual
MikeTrackers = ['device_tracker.mike_iphone_ios',
                'device_tracker.mike_iphone',]
ClaraTrackers = ['device_tracker.clara_iphone_ios',
                 'device_tracker.clara_iphone']
MikeyTrackers = ['device_tracker.mikey_iphone']
BryanTrackers = ['device_tracker.bryan_iphone']

# Get the entity that triggered the automation
triggeredEntity = data.get('entity_id')

# if the triggering entity is the meta device tracker then we need to
#   use most recent tracker for that person
if triggeredEntity == 'device_tracker.mike_meta':
    bestEntity = MikeTrackers[0]
    last_changed = hass.states.get(bestEntity).last_changed
    for entity in MikeTrackers:
        state = hass.states.get(entity)
        if state != None:
            if state.last_changed > last_changed:
                bestEntity = entity
                last_changed = state.last_changed
elif triggeredEntity == 'device_tracker.clara_meta':
    bestEntity = ClaraTrackers[0]
    last_changed = hass.states.get(bestEntity).last_changed
    for entity in ClaraTrackers:
        state = hass.states.get(entity)
        if state != None:
            if state.last_changed > last_changed:
                bestEntity = entity
                last_changed = state.last_changed
elif triggeredEntity == 'device_tracker.mikey_meta':
    bestEntity = MikeyTrackers[0]
    last_changed = hass.states.get(bestEntity).last_changed
    for entity in MikeyTrackers:
        state = hass.states.get(entity)
        if state != None:
            if state.last_changed > last_changed:
                bestEntity = entity
                last_changed = state.last_changed
elif triggeredEntity == 'device_tracker.bryan_meta':
    bestEntity = BryanTrackers[0]
    last_changed = hass.states.get(bestEntity).last_changed
    for entity in BryanTrackers:
        state = hass.states.get(entity)
        if state != None:
            if state.last_changed > last_changed:
                bestEntity = entity
                last_changed = state.last_changed
else:
    bestEntity = triggeredEntity

# update triggeredEntity
triggeredEntity = bestEntity

# Set friendly name and the metatracker name based on the entity that triggered
if triggeredEntity in MikeTrackers:
    newFriendlyName = 'Mike'
    newEntityPicture = '/local/mike.jpg'
    metatrackerName = 'device_tracker.mike_meta'
elif triggeredEntity in ClaraTrackers:
    newFriendlyName = 'Clara'
    newEntityPicture = '/local/clara.jpg'
    metatrackerName = 'device_tracker.clara_meta'
elif triggeredEntity in MikeyTrackers:
    newFriendlyName = 'Mikey'
    newEntityPicture = '/local/mikey.jpg'
    metatrackerName = 'device_tracker.mikey_meta'
elif triggeredEntity in BryanTrackers:
    newFriendlyName = 'Bryan'
    newEntityPicture = '/local/bryan.jpg'
    metatrackerName = 'device_tracker.bryan_meta'
else:
    newFriendlyName = None
    metatrackerName = None

# Get current & new state
newState = hass.states.get(triggeredEntity)
currentState = hass.states.get(metatrackerName)

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
    newStatus = newState.state
else:
    newStatus = currentState.state

# Create device_tracker.meta entity
hass.states.set(metatrackerName, newStatus, {
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
