def normalize_sound(sound):
    # Normalize the sound to a range of -1.0 to 1.0
    max_amplitude = max(abs(sample) for sample in sound)
    if max_amplitude == 0:
        return sound
    return [sample / max_amplitude for sample in sound]

def apply_effects(sound, effects):
    # Apply a list of effects to the sound
    for effect in effects:
        if effect == 'reverb':
            sound = apply_reverb(sound)
        elif effect == 'delay':
            sound = apply_delay(sound)
    return sound

def apply_reverb(sound):
    # Simple reverb effect implementation
    return sound  # Placeholder for actual reverb logic

def apply_delay(sound):
    # Simple delay effect implementation
    return sound  # Placeholder for actual delay logic