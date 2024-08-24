symbols = ['{', '}', '"', '\n']     # single-char keywords
other_symbols = ['/*', '*/']        # multi-char keywords
meta_keywords = ['\\meta', '\\papersize', '\\title', '\\subtitle', '\\composer']
score_keywords = ['\\score', '\\header', '\\layout', '\\staff', '\\displayName', '\\westernNotation', '\\voice', '\\right', '\\left', '\\time', '\\dotValue']
keywords = meta_keywords + score_keywords
KEYWORDS = symbols + other_symbols + keywords

def tokenize(text):
	token = ''
	tokens = []
	for i, char in enumerate(text):
		if (not char.isspace()) or char == '\n':
			token += char
    
		if (i+1) < len(text):
			if (text[i+1].isspace() or text[i+1] in KEYWORDS or token in KEYWORDS) and (token != ''):
				tokens.append(token)
				token = ''

	return tokens

def parse(tokens):
	
	return

exampleText = '''
\\meta {
	\\papersize letter
	\\title "Asalato Notation Examples"
	\\subtitle "with Western musical notation"
	\\composer "compiled by Sebastian Zhang"
}

\\score {
	\\header "Flip-Flop -> Triplet Den-Den"
	\\layout {
		\\staff "Player 1" {
			\\displayName false
		}
		\\staff "Player 1" {
			\\displayName false
			\\westernNotation true
		}
	}

	\\voice "Player 1" {
		\\right {
			\\time 4/4
			\\dotValue 8
			fi..fo....
			fi..fo....
			\\dotValue 6
			fi.fo.fi.
			fo.fi.fo.
		}

		\\left {
			/* time and dotValue inferred */
			....fi..fo
			....fi..fo
			/* dotValue inferred */
			.fi.fo.fi
			.fo.fi.fo
		}
	}
}
'''

tokens = tokenize(exampleText)

print(tokens)