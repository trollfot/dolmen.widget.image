===================
dolmen.widget.image
===================

`dolmen.widget.image` is a thin layer above `dolmen.widget.file`
providing a widget suitable to fields implementing IImageField. It
adds, thanks to `dolmen.thumbnailer` a preview of the uploaded image
in both input and display mode.

Example
=======

We are going to develop here a small example, to demonstrate the use
of `dolmen.widget.image`. First, we instanciate our test model and add
an image field to the object::

  >>> import dolmen.file
  >>> import grokcore.component as grok
  >>> from dolmen.widget.image.tests import Mammoth
  >>> from zope.interface import Interface, alsoProvides
  >>> from zope.schema.fieldproperty import FieldProperty

  >>> class IMammothId(Interface):
  ...   """Even mammoths need an ID card"""
  ...   picture = dolmen.file.ImageField(title=u'Luggages')

  >>> manfred = Mammoth()
  >>> manfred.picture = None
  >>> alsoProvides(manfred, IMammothId)

The picture is now set on our Mammoth. We create a form to try and
edit the picture field::

  >>> from megrok.z3cform.base import EditForm

  >>> class EditMammoth(EditForm):
  ...    grok.name('edit')
  ...    grok.context(IMammothId)

  >>> grok.testing.grok_component('edit', EditMammoth)
  True

We persist our Mammoth to get a located mammoth with an URL::

  >>> root = getRootFolder()
  >>> root['manfred'] = manfred
  >>> manfred = root['manfred']

We can call the edit form on our persisted object::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  
  >>> request = TestRequest()

  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets() 
  >>> print form.widgets['picture'].render() 
  <div id="form-widgets-picture"
       class="image-widget required imagefield-field">
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
    <input type="file" id="form-widgets-picture-input"
           name="form.widgets.picture" />
  <BLANKLINE>
  <BLANKLINE>
  </div>
  <BLANKLINE>

Now, let's try with a fake value::
     
  >>> manfred.picture = "some fake image"
  >>> form = getMultiAdapter((manfred, request), name='edit')
  >>> form.updateWidgets() 

  >>> print form.widgets['picture'].render() 
  <div id="form-widgets-picture"
       class="image-widget required imagefield-field">
  <BLANKLINE>
    <div class="image-widget-preview">
      <img src="http://127.0.0.1/manfred/++thumbnail++picture.preview" />
    </div>
  <BLANKLINE>
    <span>
      <a href="http://127.0.0.1/manfred/++download++picture"></a>
      <span class="discreet">
        &mdash;
  <BLANKLINE>
      </span>
    </span>
    <div style="padding-top: 1em;">
      <input type="radio" value="nochange" checked="checked"
             class="noborder"
             name="form.widgets.picture.nochange"
             onclick="document.getElementById('form-widgets-picture-input').disabled=true"
             id="form-widgets-picture-nochange" />
  <BLANKLINE>
      <label for="form-widgets-picture-nochange">Keep existing file</label>
      <br />
      <input type="radio" value="delete" class="noborder"
             name="form.widgets.picture.nochange"
             onclick="document.getElementById('form-widgets-picture-input').disabled=true"
             id="form-widgets-picture-delete" />
      <label for="form-widgets-picture-delete">Delete existing file</label>
      <br />
      <input type="radio" name="form.widgets.picture.nochange"
             onclick="document.getElementById('form-widgets-picture-input').disabled=false"
             id="form-widgets-picture-replace" />
      <label for="form-widgets-picture-replace">Replace with new file</label>
    </div>
    <input type="file" id="form-widgets-picture-input"
           name="form.widgets.picture" />
  <BLANKLINE>
    <script type="text/javascript">document.getElementById('form-widgets-picture-input').disabled=true;</script>
  </div>
  <BLANKLINE>

With non persistent objects (which don't resolve to an URL), no
preview is displayed. If we can't resolve to an URL, we can't serve
the thumbnail or download the data::

  >>> judith = Mammoth()
  >>> judith.picture = "Fake image data"
  >>> alsoProvides(judith, IMammothId)

  >>> form = getMultiAdapter((judith, request), name='edit')
  >>> form.updateWidgets() 
  >>> print form.widgets['picture'].render() 
  <div id="form-widgets-picture"
       class="image-widget required imagefield-field">
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
  <BLANKLINE>
    <div style="padding-top: 1em;">
      <input type="radio" value="nochange" checked="checked"
             class="noborder"
             name="form.widgets.picture.nochange"
             onclick="document.getElementById('form-widgets-picture-input').disabled=true"
             id="form-widgets-picture-nochange" />
  <BLANKLINE>
      <label for="form-widgets-picture-nochange">Keep existing file</label>
      <br />
  <BLANKLINE>
      <label for="form-widgets-picture-delete">Delete existing file</label>
      <br />
      <input type="radio" name="form.widgets.picture.nochange"
             onclick="document.getElementById('form-widgets-picture-input').disabled=false"
             id="form-widgets-picture-replace" />
      <label for="form-widgets-picture-replace">Replace with new file</label>
    </div>
    <input type="file" id="form-widgets-picture-input"
           name="form.widgets.picture" />
  <BLANKLINE>
    <script type="text/javascript">document.getElementById('form-widgets-picture-input').disabled=true;</script>
  </div>
  <BLANKLINE>
