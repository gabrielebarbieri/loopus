from music21 import scale

LOWER_PITCH = 'c0'
MIDDLE_PITCH = 'c4'
HIGHER_PITCH = 'c8'


class Scale(object):

    def __init__(self, name='major', tonic=MIDDLE_PITCH):
        self.name = name
        self._tonic = tonic
        self.scale = getattr(scale, f'{name.title()}Scale')(tonic)
        self.higher_pitches = self.scale.getPitches(tonic, HIGHER_PITCH)
        self.lower_pitches = self.scale.getPitches(LOWER_PITCH, tonic)[:-1]  # do not repeat the tonic!

    @property
    def tonic(self):
        return self._tonic

    @tonic.setter
    def tonic(self, tonic):
        self.scale = getattr(scale, f'{self.name.title()}Scale')(tonic)
        self.higher_pitches = self.scale.getPitches(tonic, HIGHER_PITCH)
        self.lower_pitches = self.scale.getPitches(LOWER_PITCH, tonic)[:-1]  # do not repeat the tonic!

    def __getitem__(self, item):
        if item >= 0:
            return self.higher_pitches[item]
        return self.lower_pitches[item]


default = Scale()


def print_available_scales():
    import re
    for name in dir(scale):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        if s1.endswith('_scale') and not s1.startswith('abstract'):
            s1 = s1.replace('_scale', '')
            print(s1)
