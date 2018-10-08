SOURCE_DECLENSION = 'de-declin' #remove this; it's redundant
# from aqt import mw
import os, sys
sys.path.insert(0, os.path.abspath("."))

from reedanki import HC_EXAMPLE_DICT, convert_note
from pprint   import pprint as pp


# action = QAction("Philip 2", mw)
# action.triggered.connect(main)
# mw.form.menuTools.addAction(action)
from aqt import mw
try:
  import all_tenses as at
except:
  print("Why on earth can't I load all_tenses? I've tried various ways.")
  # showInfo("Why on earth can't I load all_tenses? I've tried various ways.")

#Trying to debug an Anki plugin is.... challenging.
# I've not yet gotten Anki via PyCharm to run properly although that is 
# probably worth pursuing.
"""
Heaven only knows what 'did' is supposed to stand for; the choice of var
names in Anki is quite different from the sort of names I would have
used."""

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
    showInfo(msg)
    return notes

  def repr_of_Cloze(self):
    col=self.col
    byname = col.models.byName("Cloze")
    print(byname['id'])
    print(byname.keys())
    showInfo(
      "id is {}\n {}".format(byname['id'], 
      byname.__repr__())
      # byname.keys())
    )
  
  @classmethod
  def try_all_ids(cls):
    col = mw.col
    just_id = 1443392136631 #The one that works for lookup by mid
    did = 1502821212137
    mod = 1537162533
    lens = [
      len(col.findNotes("mid:%d" % (just_id))), #16
      len(col.findNotes("mid:%d" % (did))), #0
      len(col.findNotes("mid:%d" % (mod))), #0
    ]
    msg = col.findNotes("mid:%d" % (just_id)).__repr__()
    showInfo(msg)



h = AnkiHelper()
# AnkiHelper.try_all_ids()  #plain id is what we want.
# h.repr_of_Cloze()  #works
h.notes_for_id(h.value_for_model_name_and_key("Cloze", 'id')) #16 notes
# h.foo(1342704714050L)

class InitialLetterDestroyer():
  """I imported a shared German deck that has tags for 'A-initial-letter', 
  'B-initial-letter', and so forth. I don't see much point to those and I can
  always automate recreating them if needed, but they take up a lot of screen
  real estate"""
  current_deck = mw.col
  @classmethod
  def go (cls):
    pass

InitialLetterDestroyer.go()
  
def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
  msg = "convert_notes_of_model() is a little too spaghetti code for us to use right now, but come back to this."
  showInfo(msg)
  raise msg

def convert_notes_hardcoded_model():
  source_model_id = SOURCE_DECLENSION_MODEL
  dest_model_id = source_model_id
  old_patt="(.*) (.*)\. (.*)\. (.*)\."
  new_fields=HC_EXAMPLE_DICT.keys()

  all_source_note_ids = mw.col.findNotes("mid:%d" % source_model_id)
  THROTTLE = 2
  all_source_note_ids = all_source_note_ids[0 : THROTTLE]
  rv_notes = [convert_note(id, old_patt, new_fields) for id in all_source_note_ids]
  return rv_notes
  
  

## GUI STUFF
#create_a_label removed from here to reedanki.
#mw.setCentralWidget(label) 

  
#MW=mw
def do_dumb_shit():
  action = QAction("A bogus item " + datetime.datetime.now().strftime("%I:%M%p "), mw)
  action.triggered.connect(dir)
  # mw.form.menuTools.addAction(action)
  
  create_a_label("PHILIP", 100)
  create_a_label("HEY", 150)
  create_a_label("THERE", 200)
  create_a_label("WHAT", 250)
  
def convert_notes_hardcoded_model_and_show_msg():
  list_of_counts = convert_notes_hardcoded_model()
  showInfo("convert_notes_hardcoded_model \n %s" % list_of_counts)


#Diagnostic
# all_source_note_ids = mw.col.findNotes("mid:%d" % SOURCE_DECLENSION_MODEL)
# id = all_source_note_ids[0]
# old_patt="(.*) (.*)\. (.*)\. (.*)\."
# new_fields=HC_EXAMPLE_DICT.keys()
# rv=convert_note(id, old_patt, new_fields)
# showInfo(str(rv))

# try: 
  # assert_intended_model(SOURCE_DECLENSION_MODEL)
# except:
  # showInfo("Bad model %s" % mw.col.models.current()['id'])


# rv = create_hardcoded_note()
# assert rv > 0

# showInfo("Worked even better!")


#HOW TO ACTUALLY CHANGE THE CURRENT DECK
#See the code here: 
#https://github.com/dae/anki/blob/master/aqt/modelchooser.py

# m = self.deck.models.byName(ret.name)
# self.deck.conf['curModel'] = m['id']
# cdeck = self.deck.decks.current()
# cdeck['mid'] = m['id']
# self.deck.decks.save(cdeck)

#In our environment it's like this:         
# s = 'Cloze'
# m = mw.col.models.byName(s)
# cdeck = mw.col.decks.current()
# cdeck['mid']= m['id']
# rv=mw.col.decks.save(cdeck)        
#END HOW TO ACTUALLY CHANGE THE CURRENT DECK

#### Other old bloated stuff
# def old_convert_note(note_id, patt, new_fields):
  # note = mw.col.getNote(note_id)
  # the_match = re.match(patt, note['Front'])
  # if (not the_match):
    ##showInfo("Could not match %s with %s" % (patt, note['Front'] ))
    # return (None, 'No equivalent')


  # the_dict = {}
  # new_note=make_new_declension_note()
  # for i in range(1,5):
    # try:
      # new_note[new_fields[i-1]] = the_match.group(i)
    # except KeyError:
      # print( "You probably used a note type without a field for " + new_fields[i-1])
      # silly_keys(new_note.keys()) 

      # raise
  # global _logstring
  # _logstring += "\nstr is %s\n" % str
  # mw.col.log("str is %s" % str)
  
  # new_note['Front'] += "SYNTHETIC: "
  # new_count = mw.col.addNote(new_note)

  # _logstring += ("new count of notes is %d\n" % new_count)
  # return (new_note, str)
  
