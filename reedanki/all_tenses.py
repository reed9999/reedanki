### 
# This doesn't yet save as it seems it should.
# For now just paste this directly in the REPL 
# (Ctrl+Shift+; in Anki)

from aqt import mw

class AllTenses:
    def __init__(self, model_name='ALLTENSES'):
        self._model_name = model_name

    def lookup_and_set_model_id(self):
        self._model_id = mw.col.models.byName(self._model_name)

    def go(self):
        self.lookup_and_set_model_id()
        if self._model_id is not None: 
            mw.col.models.byName(self._model_name).delete() #untested
        new_model = mw.col.models.new(self._model_name)
        result = mw.col.models.save(m=new_model)
        print ("Saved it")
        print ("model = {}".format(new_model))
        print ("result {}".format(result))

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
at = AllTenses()
at.go()
