from random import choice
import urwid
import sys
import csv


class Flashcard(object):

    def __init__(self, definitions):
        self.definitions = self._load(definitions)
        self.show_answer = True
        self.current_term = choice(self.definitions.items())
        self.term = urwid.Text('Press any key to start', align='center')
        self.definition = urwid.Text('Press any key to start', align='center')

    def handle_key(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        self.progress()

    def progress(self):
        if not self.show_answer:
            self.term.set_text(self.current_term[0])
            self.definition.set_text(self.current_term[1])
            self.current_term = choice(self.definitions.items())
            self.show_answer = True
        else:
            hide_term = choice([True, False])
            if hide_term:
                self.term.set_text('???')
                self.definition.set_text(self.current_term[1])
            else:
                self.term.set_text(self.current_term[0])
                self.definition.set_text('???')
            self.show_answer = False

    def _load(self, filename):
        definitions = dict()
        with open(filename, 'r') as f:
            try:
                csv_reader = csv.reader(f.readlines())
                for line in csv_reader:
                    definitions[line[0]] = line[1]
            except IndexError:
                print('Incorrectly formatted CSV file')
                sys.exit(1)
        return definitions

    def run(self):
        term_box = urwid.LineBox(urwid.Filler(self.term), title='Term')
        def_box = urwid.LineBox(urwid.Filler(
            self.definition), title='Definition')
        pile = urwid.Pile([term_box, def_box])
        loop = urwid.MainLoop(pile, unhandled_input=self.handle_key)
        loop.run()


if __name__ == '__main__':
    if any([x for x in sys.argv if x in ('-h', '--help')]) \
            or len(sys.argv) < 2:
        print('Usage:')
        print('  {} <definitions>'.format(__file__))
        sys.exit(1)
    else:
        Flashcard(sys.argv[1]).run()
