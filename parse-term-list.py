import yaml
import sys
import regex as re
from slugify import slugify

def getKey(item):
    return item['term']

class Outputter:
    def __init__(self, fileName, outputFormat):
        self.firstLetter = ''
        self.outputFormat = outputFormat
        with open(fileName) as f:
            data = yaml.safe_load(f)
            filteredTerms = filter(lambda term: term[outputFormat], data['terms'])
            self.terms = sorted(filteredTerms, key=lambda t: t['term'])

            # Get a list of term names in descending size order so we match the longest terms first
            self.termNames = [t['term'] for t in self.terms]
            self.termNames.sort(key=lambda s: (len(s), s), reverse=True)

    def generateOutput(self):
        [self.outputTerm(t) for t in self.terms]

    def outputTerm(self, term):
        # Print the letter headings "## A", "## B" etc
        currentLetter=term['term'][:1]
        if currentLetter.lower() != self.firstLetter:
            print('## %s' % currentLetter)
            print('')
            self.firstLetter=currentLetter.lower()

        # Print the term and its definition
        print('### %s' % (term['term'],) )
        print('')
        self.outputDefinitionWithCrossLinks(term)
        print('')
        if self.outputFormat == 'contributor-guide' and 'usage' in term:
            print(term['usage'])

    # Add links to other terms in the term list
    # Only link first instance in definition and preserve original case
    def outputDefinitionWithCrossLinks(self, currentTerm):
        definition = currentTerm['definition']
        for t in self.termNames:

            # Don't link a term to itself
            if t.lower() != currentTerm['term'].lower():

                # Get the first instance that isn't in an existing link
                # Note: Requires regex module instead of re to work
                regexp = "(?<!\[[\w\s\-]*)%s(?![\w\s\-]*\))" % t.lower()
                m1 = re.search(regexp, definition.lower())

                if m1:
                    start = m1.span()[0]
                    end = m1.span()[1]
                    if definition[end] == 's':
                        end = end+1
                    definition = "%s[%s](#%s)%s" % (definition[:start], definition[start:end], slugify(t), definition[end:] )
        print(definition)

inputFile = sys.argv[1]    # YAML term list file
outputFormat = sys.argv[2] # customer-facing|contributor-guide

print('Processing file: %s' % inputFile)
print('Output format: %s' % outputFormat)

o = Outputter(inputFile, outputFormat)
o.generateOutput()
