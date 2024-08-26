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

The metadata section of the document is used to define high-level information, such as the composer, title, and papersize.

```
\meta {
  \papersize letter
  \title "My First Score"
  \subtitle "with western notation"
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
  \segment {
    ...
  }
}
```

##### Score Layout

The layout section of the score allows you to define how you want your different musical "voices" to appear on the document. This is done by defining staffs, each corresponding to exactly one voice. Note, one voice can have multiple staves (e.g. one for traditional notation and one for western notation).

If a staff isn't associated with a voice, it _will not_ appear in the rendered score.

```
\layout {
  \staff "Player 1" {
    \displayName true           # if set to true, renders voice name (Player 1) before staff in document (defaults to true)
    \westernNotation true       # if set to true, renders western notation instead of traditional notation (defaults to false)
  }
  \staff "Player 2" {
    \displayName true
    \westernNotation false
  }
}
```

##### Score Segment

Each score segment contains information about different voices (players) and can have exactly one time signature and dot value associated with it. For changes in time signature or dot value, a new segment will need to be defined.

Note, inside the `\left` and `right` sections is where notes will be defined. More information on that can be found in the Asalato Notation section below

```
\segment {
  \time 6/8     # time signature is 4/4
  \dotValue 8   # each note will get an eigth-note

  \voice "Player 1" {
    \right {              # defines all of the notes played in the right-hand
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
}
```

##### Asalato Notation

The full list of supported Asalato notes is included below:

| Name            | Notation | Parameters                          |
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
| flip throw      | FI\*(#)  | # is the number of flips (e.g. 0.5) |
| flop throw      | FO\*(#)  | # is the number of flips (e.g. 0.5) |
| airturn throw   | AT\*(#)  | # is the number of flips (e.g. 0.5) |
| rest            | .        |                                     |
| shake           | \|       |                                     |
| catch           | x        |                                     |
