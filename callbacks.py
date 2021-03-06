import gi
from gi.repository import GObject as gobject

def hide_widget(widget, data):
    data.hide()

def show_widget(widget, data):
    data.show()

def show_hide(widget, data):
	"""Used for showing one widget and hiding another simultaneously."""
	main_box = data[0]
	remv_box = data[1]
	which = data[2]

	if which == 'add':
		main_box.show()
		remv_box.hide()
	if which == 'des':
		main_box.hide()
		remv_box.show()

def run_widget(widget, data):
    data.run()
    data.destroy()

# Implementation functions 
def recompile(widget, data):
    timeline = data[0]
    preview = data[1]

    timeline.init_file()
    timeline.create()

    preview.set_from_file(timeline.name + '.png')
    preview.show()

def init_project(widget, data):
    textbox = data[0]
    timeline = data[2]
    name = textbox.get_text()
    timeline.set_name(name)
    data[1].hide()

def add_new_phase(widget, data):
    start_week = data[0].get_text()
    end_week = data[1].get_text()
    distance = data[2].get_value()
    color = data[3].get_text()
    size = data[4].get_value()
    timeline = data[5]
    label = data[6]

    timeline.add_phase(start_week, end_week, distance, color, size)
    label.set_text('Added.')

    # cleanup
    data[0].set_text('')
    data[1].set_text('')
    data[2].set_value(0)
    data[3].set_text('')
    data[4].set_value(0)

def set_interval(widget, data):
    weeks = data[0]
    switch = data[1]
    window = data[2]
    timeline = data[3]

    if switch.get_active():
        window.show()
    else:
        timeline.set_interval(weeks.get_text())

    switch.set_active(False)
    weeks.set_text('')

def ci_set(widget, data):
    timeline = data[10]
    custom_intervals = []
    for i in range(10):
        if data[i].get_text():
            custom_intervals.append(data[i].get_text())
    timeline.set_interval(0, True, custom_intervals)

def add_new_milestone(widget, data):
    phase = data[0].get_text()
    phase_degree = data[1].get_value()
    direction = data[2].get_value()
    length = data[3].get_text()
    placement = data[4].get_active()
    if placement == 1:
        placement = 'above'
    if placement == 2:
        placement = 'below'
    width = data[5].get_text()
    text = data[6].get_text()
    timeline = data[7]
    label = data[8]

    if not width == '':
        timeline.add_milestone(phase, phase_degree, direction,\
        length, placement, width, text)
    else:
        timeline.add_milestone(phase, phase_degree, direction,\
        length, placement, width, text, False)

    label.set_text('Added.')

    data[0].set_text('')
    data[1].set_value(0)
    data[2].set_value(0)
    data[3].set_text('')
    data[4].set_active(0)
    data[5].set_text('')
    data[6].set_text('')


def new_project(widget, data):
    timeline = data[0]
    timeline.__init__()
    window = data[1]
    textbox = data[2]
    ok = data[3]

    window.show()

    def _ok_callback(widget, data):
        data[0].set_name(data[2].get_text())
        data[1].hide()

    ok.connect('clicked', _ok_callback, data)

def label_hider(labels):
    for label in labels:
        label.hide()

    gobject.timeout_add(5000, label_hider, labels)

def reset_timeline(widget, data):
	data.__init__()
	data.init_file()

def show_remove(widget, data):
	box = data[0]
	which = data[1]
	string = data[2]

	box.show()
	which = string

def remove_phase_or_ms(widget, data):
	data[3].set_text('Removed.')
	timeline = data[0]
	try:
		index = int(data[2].get_text())
	except ValueError:
		print('Please enter a number.') # TODO make this a popup

	if data[1] == 'phase':
		timeline.remove_phase(index)
	if data[1] == 'milestone':
		timeline.remove_milestone(index)