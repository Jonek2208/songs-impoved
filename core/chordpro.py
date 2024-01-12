import re
from dataclasses import dataclass

@dataclass
class Chord:
    root: str
    qual: str
    ext: str
    bass: str

    def get_name(self):
        return f'{self.root}{self.qual if self.qual else ""}{self.ext if self.ext else ""}{f"/{self.bass}" if self.bass else ""}'

class ClassicChords:
    regex = re.compile(
        r"([A-H][b#]?)([^\]\/\s]*\/?)((?:[A-H][b#]?)?)(?:\:(\d)+(?:\/(\d)+)?)?")
    chords_table = {
        'A': 0,
        'A#': 1,
        'Bb': 1,
        'B': 2,
        'Cb': 2,
        'C': 3,
        'C#': 4,
        'Db': 4,
        'D': 5,
        'D#': 6,
        'Eb': 6,
        'E': 7,
        'F': 8,
        'F#': 9,
        'Gb': 9,
        'G': 10,
        'G#': 11,
        'Ab': 11,
    }

    keys_table = ['A', 'Bb', 'B', 'C', 'Db',
                  'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

    @classmethod
    def get_transposed_key(cls, original_key: str, transpose: int):
        return cls.keys_table[(cls.chords_table[original_key] + transpose) % 12]

    enharmonics_table = {
        'C': ('C#', 'D#', 'F#', 'G#', 'Bb'),
        'Db': ('Db', 'Eb', 'Gb', 'Ab', 'Bb'),
        'D': ('C#', 'D#', 'F#', 'G#', 'A#'),
        'Eb': ('C#', 'Eb', 'F#', 'Ab', 'Bb'),
        'E': ('C#', 'D#', 'F#', 'G#', 'A#'),
        'F': ('C#', 'Eb', 'F#', 'Ab', 'Bb'),
        'Gb': ('Db', 'Eb', 'Gb', 'Ab', 'Bb'),
        'G': ('C#', 'D#', 'F#', 'G#', 'A#'),
        'Ab': ('Db', 'Eb', 'Gb', 'Ab', 'Bb'),
        'A': ('C#', 'D#', 'F#', 'G#', 'A#'),
        'Bb': ('Db', 'Eb', 'F#', 'Ab', 'Bb'),
        'B': ('C#', 'D#', 'F#', 'G#', 'A#'),
    }

    special_chords = {
        "m7b5": "&#119209;",
        "m7(b5)": "&#119209;",
        "dim7": "<sup>o7</sup>",
        "maj7": "<small>&#916;</small>",
        "m7": "<small>m</small><sup>7</sup>",
        "m9": "<small>m</small><sup>9</sup>",
        "sus4": "<small>sus4</small>",
        "sus2": "<small>sus2</small>",
        "sus4/": "<small>sus4</small>/",
        "sus2/": "<small>sus2</small>/",
        "2": "<small>2</small>",
        "4": "<small>4</small>",
    }

    defined_chords = {
        "": (0, 4, 7),
        "m": (0, 3, 7),
        "maj7": (0, 4, 7, 11),
        "maj9": (0, 4, 7, 11, 14),
        "7": (0, 4, 7, 10),
        "m7": (0, 3, 7, 10),
    }

    notes_html = [
        ('#', "&#x266f;"),
        ("b", "&#x266d;"),
    ]

    reverse_table = [
        lambda x: 'A',
        lambda x: ClassicChords.enharmonics_table[x][4],
        lambda x: 'B',
        lambda x: 'C',
        lambda x: ClassicChords.enharmonics_table[x][0],
        lambda x: 'D',
        lambda x: ClassicChords.enharmonics_table[x][1],
        lambda x: 'E',
        lambda x: 'F',
        lambda x: ClassicChords.enharmonics_table[x][2],
        lambda x: 'G',
        lambda x: ClassicChords.enharmonics_table[x][3],

    ]

    @classmethod
    def parse_chord(cls, chord_text: str):
        m = cls.regex.match(chord_text)
        chord_letter = m.group(1)
        chord_type = m.group(2)
        chord_slash = m.group(3) if len(m.group(3)) > 0 else None
        duration_num = int(m.group(4)) if m.group(
            4) is not None and len(m.group(4)) > 0 else None
        duration_den = int(m.group(5)) if m.group(
            4) is not None and len(m.group(4)) > 0 else 1
        return chord_letter, chord_type, chord_slash, duration_num, duration_den

    @classmethod
    def transpose_note(cls, chord_letter: str, transpose: int, target_key: str):
        chord_ord = (cls.chords_table[chord_letter] + transpose) % 12
        return cls.reverse_table[chord_ord](target_key)
    
    @classmethod
    def get_note_in_key(cls, note: int, key: str):
        chord_ord = (cls.chords_table[key] + note) % 12
        return cls.reverse_table[chord_ord](key)

    @classmethod
    def render_note(cls, note: str):
        return note.replace(*cls.notes_html[0]).replace(*cls.notes_html[1])

    @classmethod
    def transpose_chord(cls, chord_text: str, transpose: int, target_key: str, bass_only: bool):
        chord_letter, chord_type, chord_slash_letter, duration_num, duration_den = cls.parse_chord(
            chord_text)
        if chord_type in cls.special_chords:
            chord_type = cls.special_chords[chord_type]
        chord_root = cls.transpose_note(chord_letter, transpose, target_key)
        chord_slash = cls.transpose_note(
            chord_slash_letter, transpose, target_key) if chord_slash_letter is not None else None
        if bass_only:
            return f"{cls.render_note(chord_root if not chord_slash else chord_slash)}"

        return f"{cls.render_note(chord_root)}{chord_type}{cls.render_note(chord_slash) if chord_slash else ''}"


class ChordPro:
    tag_re = re.compile(r'^\s*{([^:]+):?\s?([^}]*)}\s*$')
    chord_re = re.compile(r'\[([^\]]+)\]')
    space_re = re.compile(r'^\s+')

    chords_table = {
        'A': 0,
        'A#': 1,
        'Bb': 1,
        'B': 2,
        'Cb': 2,
        'C': 3,
        'C#': 4,
        'Db': 4,
        'D': 5,
        'D#': 6,
        'Eb': 6,
        'E': 7,
        'F': 8,
        'F#': 9,
        'Gb': 9,
        'G': 10,
        'G#': 11,
        'Ab': 11,
    }

    @classmethod
    def is_bar(cls, text: str):
        return text == '|'
    
    @classmethod
    def get_chord_data(cls, text: str):
        print(text)
        chord_letter, chord_type, chord_slash, *_ = ClassicChords.parse_chord(text)
        chord_notes = ClassicChords.defined_chords.get(chord_type)
        res = [ClassicChords.get_note_in_key(x, chord_letter) for x in chord_notes]
        return res

    @classmethod
    def get_line_with_chords(cls, text: str, transpose: int, target_key: str, bass_only: bool):
        data = []
        last_chord = None

        if len(text) == 0:
            return data

        while True:
            match = cls.chord_re.search(text)
            if match is None:
                break

            x, y = match.span()

            data.append({"text": text[:x], "chord": last_chord})
            text = text[y:]

            if cls.is_bar(match.group(1)):
                data.append({"bar": True})
                last_chord = None
                continue

            last_chord_raw = match.group(1)
            last_chord = ClassicChords.transpose_chord(
                last_chord_raw, transpose, target_key, bass_only)

            if cls.space_re.match(text) is None:
                data[-1]["spacer"] = True

        data.append({"text": text, "chord": last_chord})
        return data

    @classmethod
    def render_chordpro(cls, text: str, transpose: int, original_key: str, bass_only: bool):
        target_key = ClassicChords.get_transposed_key(original_key, transpose)
        lines = text.splitlines()
        result = []
        for line in lines:
            tag_match = cls.tag_re.match(line)
            if not tag_match:
                data = cls.get_line_with_chords(
                    line, transpose, target_key, bass_only)
                result.append((data, False))
            else:
                data = tag_match.group(1), tag_match.group(2)
                if data[0] == 'c':
                    result.append((data, True))

        return result
