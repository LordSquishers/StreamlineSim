import ui
import scene

class KBHandler(ui.View):
	
	def __init__(self, scene_input, **kwargs):
		super().__init__(**kwargs)
		sceneview = scene.SceneView(
			frame = self.bounds, flex='WH',
		)
		sceneview.scene = self.scene = scene_input
		self.add_subview(sceneview)
		
	def get_key_commands(self):
		return [
			# custom commands
				{'input': '\b'}, # clear! delete key
				{'input': 'right'},  # cycle right
				{'input': 'left'},  # cycle left
				
				{'input': 'up'}, # strength up
				{'input': 'down'}, # strength down
				
				{'input': 'up', 'modifiers': 'shift'}, # strength up x 5
				{'input': 'down', 'modifiers': 'shift'}, # strength down x 5	
				
				{'input': 'M'} # mode switch (add, view)
				]
	
	def key_command(self, sender):
		# process commands
		if sender['input'] == '\b':
			self.scene.clear_components()
		if sender['input'] == 'right':
			self.scene.cycle_next()
		if sender['input'] == 'left':
			self.scene.cycle_prev() 
		if sender['input'] == 'up':
			if sender['modifiers'] == 'shift':
				self.scene.change_strength(5)
			else:
				self.scene.change_strength(1)
		if sender['input'] == 'down':
			if sender['modifiers'] == 'shift':
				self.scene.change_strength(-5)
			else:
				self.scene.change_strength(-1)
		if sender['input'] == 'M':
			self.scene.change_mode()

