### 
# This doesn't yet save as it seems it should.
# For now just paste this directly in the REPL 
# (Ctrl+Shift+; in Anki)

from aqt import mw

class AllTenses:
    #All this functionality was moved to VerbNoteCreator, presently (but not 
    # forever) in reedanki.
    # Now this file is just a test of importing in anki addons, but eventually
    # I will move real functionality back and probably rename. 

    pass

def foo(id):
  col=mw.col
  n = col.findNotes("mid:%d" % (id))
  print(len(n))
def foo2():
 col = mw.col
 byname = col.models.byName("Cloze")
 print(byname['id'])
 print(byname.keys())

# print(foo(1443392136631))
if __name__ == "__main__":
    at = AllTenses()
    at.go()
