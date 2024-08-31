# Asalato Notation Software

A text-driven generator for Asalato sheet music.

## Setup

1. Ensure you have python 3.7 or later installed
2. Install all necessary libraries with the following command:

```
pip install -r ./requirements.txt
```

## Usage

To run the program, use the following command:

```
usage: main.py [-h] [--dest DEST] filename

positional arguments:
  filename              input file path

optional arguments:
  -h, --help            show this help message and exit
  --dest DEST, -d DEST  pdf output file path
```

### Notation Language

#### Metadata

The metadata section of the document is used to define high-level information, such as the composer, title, and paper properties.

```
\meta {
  \paper {
    \size letter
    \margin 0.5in             # margin to use on all sides
    \marginLeft 0.25in        # overrides default margin on a per-side basis
    \marginRight 0.25in
    \marginTop 0.75in
    \marginBottom 0.75in
  }
  \title "My First Score"
  \subtitle "with western notation" {       # all text objects can optionally specify the following properties
    \font "Calibri"                         # font family (defaults to "Arial")
    \fontSize 16                            # font size (default depends on text object)
    \fontWeight 50                          # font weight (defaults to 50, should be in range 0-100)
    \italic                                 # if added, italicizes text (defaults to False)
  }
  \composer "J.S Bach"
}
```

#### Score

Each document can have any number of scores, which is where musical notes and symbols are defined. By using mutliple scores, you can seperate your document based on movements, exercises, etc.

```
\score {
  \header "Header for this score"
  \layout {
    ...
  }
  \voice "My Voice" {
    ...
  }
}
```

##### Score Layout

The layout section of the score allows you to define how you want your different musical "voices" to appear on the document. This is done by defining staffs, each corresponding to exactly one voice. Note, one voice can have multiple staves (e.g. one for traditional notation and one for western notation).

If a staff isn't associated with a voice, it _will not_ appear in the rendered score.

```
\layout {
  \staff "Player 1"           # Note, only 1 staff is supported per score at this time
  \notationScale 1.2          # scales up/down all notes, articulations, etc. based on the provided factor
  \noteSpacing 2.0            # scales up/down the horizontal spacing between each note based on the provided factor
  \staffSpacing 1.8           # scales up/down the vertical spacing between staffs based on the provided factor
  \extendLastLine             # if added, the final line in the score will take the full width of the document
}
```

##### Score Voices

Each voice contains all relevant information about notes, as well as time signatures and dot value associations. Changes in time signature or dot value only need to be defined in one voice, and will be inferred in all other voices.

Note, inside the `\left` and `right` sections is where notes will be defined. More information on that can be found in the Asalato Notation section below

```
\voice "Player 1" {
  \right {              # defines all of the notes played in the right-hand
    \time 4/4           # time signature is 4/4
    \dotValue 1/8       # each note will get an eigth-note
    .  .  FI .  .  FO
  }

  \left {               # defines all of the notes played in the left-hand
    FI .  .  FO .  .
  }
}

\voice "Player 2" {
  \right {
    FI .  FI .  FI .
  }

  \left {
    .  FO .  FO .  FO
  }
}
```

In addition to standard notes, tuples are supported. When adding a tuple, it is important to clearly define how many dot values it should span across.

```
tuple {
  \duration 4           # 4 1/8 note lengths (1/2 measure)
  FI . FO
}
```

Each note can also have modifiers applied to it. These render additional components in-line with the given note, such as articulations, dynamics, and knocks. Each modifier should be included directly after the note it is modifying:

```
FI\ff\knock   # adds fortissimo dynamic marking and knock marking to the same note.
```

##### Asalato Notes

The full list of supported Asalato notes is included below:

| Note            | Notation | Parameters                          |
| --------------- | -------- | ----------------------------------- |
| flip            | FI       |                                     |
| flip            | FO       |                                     |
| flip grab       | FI+      |                                     |
| flop grab       | FO+      |                                     |
| click flip      | CI       |                                     |
| click flop      | CO       |                                     |
| click flip grab | CI+      |                                     |
| click flop grab | CO+      |                                     |
| den down        | DD       |                                     |
| den up          | DU       |                                     |
| den down grab   | DD+      |                                     |
| den up grab     | DU+      |                                     |
| airturn         | AT       |                                     |
| airturn_fake    | AF       |                                     |
| flip throw      | FI\*#    | # is the number of flips (e.g. 0.5) |
| flop throw      | FO\*#    | # is the number of flips (e.g. 0.5) |
| airturn throw   | AT\*#    | # is the number of flips (e.g. 0.5) |
| rest            | .        |                                     |
| shake           | \|       |                                     |
| catch           | x        |                                     |

##### Modifiers

A full list of supported note modifiers is included below:

| Asalato Notations | Notation |
| ----------------- | -------- |
| knock             | \knock   |

| Articulations    | Notation         |
| ---------------- | ---------------- |
| accent           | \accent          |
| staccato         | \staccato        |
| tenuto           | \tenuto          |
| stacatissimo     | \stacatissimo    |
| marcato          | \marcato         |
| marcato staccato | \marcatoStaccato |
| accent staccato  | \accentStaccato  |
| tenuto staccato  | \tenutoStaccato  |
| tenuto accent    | \tenutoAccent    |
| stress           | \stress          |
| unstress         | \unstress        |
| marcato tenuto   | \marcatoTenuto   |

| Dynamics    | Notation |
| ----------- | -------- |
| PPPPPP (x6) | \pppppp  |
| PPPPP (x5)  | \ppppp   |
| PPPP (x4)   | \pppp    |
| PPP (x3)    | \ppp     |
| PP          | \pp      |
| P           | \p       |
| MP          | \mp      |
| MF          | \mf      |
| F           | \f       |
| FF          | \ff      |
| FFF (x3)    | \fff     |
| FFFF (x4)   | \ffff    |
| FFFFF (x5)  | \fffff   |
| FFFFFF (x6) | \ffffff  |
