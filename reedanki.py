####
# reedanki.py -- very exploratory, ugly code with an obvious security vulnerability.
# Also way too much use of globals because I wasn't understanding how the interactive prompt
# was loading Python packages.

# From before:
# The goal is to go through a particular (later, aribtrary)
# note type, parse out the content according to a regex, and put the 
# content into a new note of a different, particular (later, arbitrary)
# note type

import datetime
from pprint   import pprint as pp
from string import ascii_uppercase
import re

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

#reload (philip.main)

SOURCE_DECLENSION = 'de-declin'
SOURCE_DECLENSION_MODEL = 1342704714050L
WEIRD_DECLENSION_MODEL = 1450932830892L
DESTINATION_DECLENSION_MODEL = SOURCE_DECLENSION_MODEL

_counter = 0
_logstring = ""

##### NEWER CODE
# Try building from the ground up--something between a refactor and an overhaul.

def dangerous_exec():
  import os
  dir = os.path.dirname(__file__)

  #https://stackoverflow.com/a/1463370/742573
  ldict = locals()
  
  filename = os.path.join(dir, 'reedanki', 'arbitrary.py')
  with open(filename, 'r') as the_file:
    exec (the_file.read(), globals(), ldict) 
  return ldict

class AnkiHelper():
  current_deck = mw.col
  col = current_deck


  def value_for_model_name_and_key(self, name, key='id'):

    model_dict = self.col.models.byName(name)
    return model_dict[key]

  def notes_for_id(self, id):
    """The id here is the plain old ['id'] value for the note, not the did or
    the mod."""
    #mid is elsewhere known as mod, because it's Anki code, that's why
    notes = self.col.findNotes("mid:%d" % (id))
    msg = "model ID is {}\nNumber of notes: {}".format(id, len(notes))
    print(msg)
    # showInfo(msg)
    return notes

  # @classmethod
  # def try_all_ids(cls):
  #   """Sort out the IDs. just_id is the most useful apparently."""
  #   col = mw.col
  #   just_id, did, mod = 1443392136631, 1502821212137, 1537162533

class BrokenInitialLetterDestroyer():
  """I imported a shared German deck that has tags for 'A-initial-letter', 
  'B-initial-letter', and so forth. I don't see much point to those and I can
  always automate recreating them if needed, but they take up a lot of screen
  real estate.
  
  I don't understand why it became unable to find mw.col (or cls.current_deck)
  after I moved this to the main reedanki.py file."""
  current_deck = mw.col
  helper = AnkiHelper()
    
  @classmethod
  def delete_tag_for_letter(cls, letter):
    tag_name = "{}-initial-letter".format(letter)
    notes = cls.current_deck.findNotes("tag:{}".format(tag_name))
    showInfo(str(len(notes)))
    
  @classmethod
  def go (cls):
    global ascii_uppercase 
    for letter in ascii_uppercase[5:25]:
      cls.delete_tag_for_letter(letter)

    # showInfo(helper.notes_for_id(0).__repr__())



###GUI
def create_a_label(text, x=25):
  label = QLabel()
  label.setText(text)
  label.setGeometry(x, x/2 , 300 , 300,)
  layout = mw.layout()
  layout.addWidget(label)
  mw.setLayout(layout)

  
def main():


#Hang onto this code somewhere because it's how I want to run dynamically in the future.
  ldict = dangerous_exec()
#  convert_notes_hardcoded_model = ldict['convert_notes_hardcoded_model']
#  rv = convert_notes_hardcoded_model()
#  assert rv > 0

  # create_a_label("I EXECUTED SOME ARBITRARY CODE", 10)

  

##### OLDER CODE

#This is redundant. See anki code,  m = self.deck.models.byName(name)
def id_for_first_model_matching(patt):
  all_models = mw.col.models.all()
  for model in all_models:
    if re.match(patt, model['name']):
      return model['id']


def get_list_from_file():
  import os
  dir = os.path.dirname(__file__)
  filename = os.path.join(dir, 'reedanki', 'config.txt')
  with open(filename) as f:
    lines = f.read().splitlines()   
  return lines

#to use create_a_label see the locals() thing below 

def make_new_declension_note():
  #This feels like it has an extra unneccessary step.
  # Could we simply mw.col.conf['curModel'] = DESTINATION_DECLENSION_MODEL???
  new_declension_id = DESTINATION_DECLENSION_MODEL
  model_we_want = mw.col.models.get(new_declension_id)
  mw.col.models.setCurrent(model_we_want)  #Does this work? Seems to require us to do it GUI anyway.
  new_note = mw.col.newNote()
  #new_note.model = model_we_want  #breaks things because Note.model apparently a different type?
  # global _counter
  # if _counter < 10:
    # showInfo("new count of notes is %d" % new_count)
  global _logstring
  _logstring += ("empty new note has been created\n")
  return new_note

  
#moved to arbitrary.py
# def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
# def convert_note(note_id, patt, new_fields):

def old_convert_note(note_id, patt, new_fields):
  note = mw.col.getNote(note_id)
  the_match = re.match(patt, note['Front'])
  if (not the_match):
    #showInfo("Could not match %s with %s" % (patt, note['Front'] ))
    return (None, 'No equivalent')


  the_dict = {}
  str = ''
  new_note=make_new_declension_note()
  for i in range(1,5):
    str += "New field %s will be %s.   " % (new_fields[i-1], the_match.group(i))
    #the_dict[new_fields[i-1]] = m.group(i)
    try:
      new_note[new_fields[i-1]] = the_match.group(i)
    except KeyError:
      print( "You probably used a note type without a field for " + new_fields[i-1])
      silly_keys(new_note.keys()) 

      raise
  # global _counter
  # if _counter < 10:
    # showInfo("str is %s" % str)
    # showInfo("new_note is %s" % new_note)
  global _logstring
  _logstring += "\nstr is %s\n" % str
  mw.col.log("str is %s" % str)
  new_count = mw.col.addNote(new_note)

  _logstring += ("new count of notes is %d\n" % new_count)
  return (new_note, str)

def silly_keys(the_keys):
  n = 100
  for a_key in the_keys:
    create_a_label(str(a_key), n)
    n += 33

    
### BAD STUFF ABOVE? NOT SURE
### PASTE IN

HC_EXAMPLE_DICT = {
    'Front': 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'Back': 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'declension_context': 'some context',
    'gender': 'm f n',
    'number': 'singular',
    'case': 'nominagenitavocative',
  }


def set_current_model(model_name=SOURCE_DECLENSION):
  model = mw.col.models.byName(model_name)
  cdeck = mw.col.decks.current()
  cdeck['mid']= model['id']
  return mw.col.decks.save(cdeck)        
  

def assert_intended_model(model_name=SOURCE_DECLENSION):
  assert mw.col.models.current()['id'] == mw.col.models.byName(model_name)['id']

def create_note(model_name, dict):
  global set_current_model
  global assert_intended_model
  set_current_model(model_name)
  #assert_intended_model(model_name)
  new_note = mw.col.newNote()
  for k, v in dict.iteritems():
    new_note[k] = v
  new_count = mw.col.addNote(new_note)
  return new_count
  
def create_hardcoded_note():
  global create_note
  dict = HC_EXAMPLE_DICT
  return create_note(SOURCE_DECLENSION, dict)

#Probably some library implementation of this?
def get_match_groups(patt, text): 
  rv = []
  match = re.match(patt, text)
  for i in range (0, 100):    #I don't really want [0] but keep for standardization
    try:
      rv.append(match.group(i))
    except:
      return rv
  showInfo("Surprising. Didn't expect 100")
  return rv
  
def dict_from(match_groups, back):
  global dict_from
  return {
    'Front': 'PHILIP dict_from front | ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'Back': back,
    'declension_context': match_groups[1],
    'gender': match_groups[2],
    'number': match_groups[3],
    'case': match_groups[4],
  }

def convert_note(note_id, patt, new_fields):
  global SOURCE_DECLENSION
  global get_match_groups
  src_note = mw.col.getNote(note_id)
  match_groups = get_match_groups(patt, src_note['Front'])
  new_count = create_note(SOURCE_DECLENSION, dict_from(match_groups, src_note['Back']))
  return new_count
    

action = QAction("Philip: Run arbitrary.py", mw)
action.shortcut = QKeySequence('p')
action.triggered.connect(main)
mw.form.menuTools.addAction(action)



