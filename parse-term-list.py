import yaml
import sys
import regex as re
from slugify import slugify

services = {'iot-hub':'Iot Hub','iot-central':'IoT Central','iot-fundamentals':'IoT fundamentals','iot-dps':'Device Provisioning Service','iot-edge':'IoT Edge','digital-twins':'Digital Twins','iot-develop':'Device developer'}

class Outputter:
    def __init__(self, fileName, outputFormat):
        self.firstLetter = ''
        self.outputFormat = outputFormat
        with open(fileName) as f:
            data = yaml.safe_load(f)
            if outputFormat in ['customer-facing', 'contributor-guide']:
                filteredTerms = filter(lambda term: term[outputFormat], data['terms'])
            else: #dump-all
                filteredTerms = data['terms']
            self.terms = sorted(filteredTerms, key=lambda t: t['term'])

            # Get a list of term names in descending size order so we match the longest terms first
            # This list is used for cross-linking terms in termlist
            self.termNames = [t['term'] for t in self.terms]
            self.termNames.sort(key=lambda s: (len(s), s), reverse=True)

    def generateOutput(self):
        [self.outputTerm(t) for t in self.terms]

    def outputTerm(self, term):
        currentLetter=term['term'][:1]
        definition=self.addCrossLinksToTerm(term)
        serviceList = ''
        for s in term['services']:
            serviceList = '%s, %s' % (serviceList, services[s])

        if self.outputFormat == 'customer-facing':
            # Print the letter headings "## A", "## B" etc            
            if currentLetter.lower() != self.firstLetter:
                print('## %s' % currentLetter)
                print('')
                self.firstLetter=currentLetter.lower()

            # Print the term and its definition
            print('### %s\n' % (term['term'],) )
            print(definition)
            if 'learn-more' in term:
                print('[Learn more](%s)\n' % term['learn-more'])
            print ('Applies to: %s\n' % serviceList[2:])

        if self.outputFormat == 'contributor-guide':
            # Print the letter headings "## A", "## B" etc
            if currentLetter.lower() != self.firstLetter:
                print('## %s' % currentLetter)
                print('')
                self.firstLetter=currentLetter.lower()

            # Print the term and its definition
            print('### %s\n' % (term['term'],) )
            print('Applies to: %s\n' % serviceList[2:])
            print(definition)
            if 'usage' in term:
                self.outputUsage(term['usage'])

            
        if self.outputFormat == 'dump-all':
            if 'usage' in term:
                self.outputUsage(term['usage'])
            if 'learn-more' in term:
                print('[Learn more](%s)\n' % term['learn-more'])
            serviceList = ''
            for s in term['services']:
                serviceList = '%s, %s' % (serviceList, services[s])
            print ('Applies to: %s' % serviceList[2:])


    def outputUsage(self, term):
        if 'casing-rules' in term:
            print('Casing rules: %s' % (term['casing-rules']))
            print('')
        if 'first-mention' in term:
            print('First mention: %s' % (term['first-mention']))
            print('')
        if 'accepted-abbreviation' in term:
            print('Abbreviation: %s' % (term['accepted-abbreviation']))
            print('')
        if 'example-usage' in term:
            print('Example usage: %s' % (term['example-usage']))
            print('')

    # Add links to other terms in the term list
    # Only link first instance in definition and preserve original case
    def addCrossLinksToTerm(self, currentTerm):
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
        return definition

inputFile = sys.argv[1]    # YAML term list file
outputFormat = sys.argv[2] # customer-facing|contributor-guide|dump-all

print('Processing file: %s' % inputFile)
print('Output format: %s' % outputFormat)

o = Outputter(inputFile, outputFormat)
o.generateOutput()
