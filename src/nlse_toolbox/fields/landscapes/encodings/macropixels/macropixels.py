from .region import feature_macropixel
from .continuous_encodings import amplitude_encoding, phase_encoding


def continuous_macropixels(
    mesh,
    fs,
    sizes,
    encodings,
):
    macropixels = {}
    for key in fs.keys():
        # create empty macropixel region
        macropixels[key] = feature_macropixel(mesh, sizes)
        
        # encode feature
        if (encodings[key].lower()=="amplitude"):
            macropixels[key] = amplitude_encoding(fs[key], macropixels[key])
        elif (encodings[key].lower()=="phase"):
            macropixels[key] = phase_encoding(fs[key], macropixels[key])
    return macropixels