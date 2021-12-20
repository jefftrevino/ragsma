from math import log
from functools import reduce

import abjad

class PathwayPitch:
    def __init__(self, base_frequency, sequence_of_factors):
        multiplier = reduce(lambda x, y: x * y, sequence_of_factors)
        self.frequency = base_frequency * multiplier
        equal_tempered_base = 1.059463
        equal_tempered_power = log(self.frequency / 440, equal_tempered_base)
        self.closest_equal_tempered_pitch_number = 9 + round(equal_tempered_power)
        self.closest_equal_tempered_pitch_frequency = pow(equal_tempered_base, round(equal_tempered_power)) * 440
        self.cents_difference = self._calculate_cents_difference()
        self.notehead_pitch = abjad.NumberedPitch(self.closest_equal_tempered_pitch_number)
        self.cents_difference = self._calculate_cents_difference()
    
    def _calculate_cents_difference(self):
        difference = self.frequency - self.closest_equal_tempered_pitch_frequency
        cents = abs(1200 * (log(self.closest_equal_tempered_pitch_frequency / self.frequency)/ log(2)))
        if 0 < difference:
            return cents
        elif 0 > difference:
            return -1 * cents

    def note(self, duration):
        note = abjad.Note(self.notehead_pitch, duration)
        self._add_markup_to_note(note)
        return note
    
    def _add_markup_to_note(self, note):
        if self.cents_difference:
            markup = abjad.Markup(self.cents_difference, direction=abjad.Up)
            abjad.attach(markup, note)

if __name__ == '__main__':
    pitch = PathwayPitch(440, [1/2, 1/2, 2/3])
    print(pitch.notehead_pitch)
    print(pitch.cents_difference)
    note = pitch.note((1,4))
    print(abjad.lilypond(note))