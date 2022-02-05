import numpy as np
import matplotlib.pyplot as plt
from source import Source, Vortex, Doublet
import ui
import keyboard
from scene import *
from keyboard_handler import KBHandler

# TODO: hightlight equal potential lines, interactive graph (move and zoom)

wx = [-2, 2]
wy = [-1.5, 1.5]

DEFAULT_STRENGTH = 1
STAGNATION_POINT_TOLERANCE = 0.15

Y, X = np.mgrid[wy[0]:wy[1]:100j, wx[0]:wx[1]:100j]

sources = [Source(0, 0, 0), Vortex(0, 0, 0), Doublet(0, 0, 0)]


def calculate_fluid():
	# vector fields
	u = 1  # streamline of strength 1 in x+ direction
	v = 0

	for src in sources:
		su, sv = src.evaluate(X, Y)
		u = u + su
		v = v + sv

	stagnation_points = [[], []]

	X_step = (wx[1] - wx[0]) / 100.0
	current_x = wx[0]
	i = 0
	j = 0

	for u0 in u:
		for ux in u0:
			if abs(ux) < STAGNATION_POINT_TOLERANCE and abs(
					v[i, j]) < STAGNATION_POINT_TOLERANCE:
				# print(current_x, Y[i, j])
				stagnation_points[0].append(current_x)
				stagnation_points[1].append(Y[i, j])
			#if abs(current_x) < 0.05 and abs(Y[i, j]) < 0.05:
			#print(ux, v[i, j])
			current_x = current_x + X_step
			j = j + 1
		current_x = wx[0]
		j = 0
		i = i + 1

	# Varying color along a streamline
	fig = plt.figure(figsize=(12, 7))

	plt.xlim(wx)
	plt.ylim(wy)

	strm = plt.streamplot(X, Y, u, v, color=u, linewidth=1.5, cmap='summer')
	fig.colorbar(strm.lines)

	for src in sources:
		if src.strength == 0:
			continue
		plt.scatter(src.x0, src.y0)

	plt.xlabel('x')
	plt.ylabel('y')

	plt.title('Incompressible Fluid Simulation')
	plt.text(-1.25, wy[0] - 0.5,
										'[Source | Sink | AC Vortex | C Vortex | Doublet | Clear]')
	plt.scatter(
		stagnation_points[0], stagnation_points[1], color='red', marker='x')

	plt.savefig('result.png')
	return (u, v)


def locate_velocity_values(xpos, ypos, u, v):
	out_u = 0
	out_y = 0
	
	X_step = (wx[1] - wx[0]) / 100.0
	current_x = wx[0]
	i = 0
	j = 0
	
	us = []
	vs = []

	for u0 in u:
		for ux in u0:
			if abs(xpos - current_x) < 0.05 and abs(ypos - Y[i, j]) < 0.05:
				# print(current_x, Y[i, j])
				us.append(ux)
				vs.append(v[i, j])
			current_x = current_x + X_step
			j = j + 1
		current_x = wx[0]
		j = 0
		i = i + 1
	
	out_u = np.average(np.array(us))
	out_v = np.average(np.array(vs))
	
	return (out_u, out_v)


class TheScene(Scene):
	def setup(self):

		# vars
		self.current_strength = DEFAULT_STRENGTH
		
		self.selected_choice = 0
		self.choices = ['Source', 'Sink', 'Doublet', 'Vortex']
		
		self.selected_mode = 0
		self.modes = ['Add', 'Inspect']
		
		self.u = 0
		self.v = 0
		
		# UI elements
		self.graphimage = SpriteNode(Texture(ui.Image.named('result.png')), scale=0.5)
		self.graphimage.position = self.size / 2
		self.add_child(self.graphimage)

		self.choice_label = LabelNode('Selected: ' +
																																self.choices[self.selected_choice])
		self.choice_label.position = self.size / 2
		self.choice_label.position = self.choice_label.position - (0, 315)
		self.add_child(self.choice_label)

		self.strength_label = LabelNode('Strength: ' + str(self.current_strength))
		self.strength_label.position = self.size / 2
		self.strength_label.position = self.strength_label.position - (0, 350)
		self.add_child(self.strength_label)
		
		self.mode_label = LabelNode('Mode: ' + self.modes[self.selected_mode])
		self.mode_label.position = self.size / 2
		self.mode_label.position = self.mode_label.position - (400, 300)
		self.add_child(self.mode_label)
		
		self.inspect_label = LabelNode('(0.000, 0.000) <0.000, 0.000>')
		self.inspect_label.position = self.size / 2
		self.inspect_label.position = self.inspect_label.position - (390, 400)
		self.add_child(self.inspect_label)

	def refresh_graph(self):
		self.graphimage.remove_from_parent()
		self.graphimage = SpriteNode(
			Texture(ui.Image.named('result.png')), scale=0.5)
		self.graphimage.position = self.size / 2
		self.graph_node = self.add_child(self.graphimage)

	def touch_began(self, touch):
		x, y = touch.location

		gx_length = wx[1] - wx[0]
		gy_length = wy[1] - wy[0]

		# coordinates experimentally calculated.
		x = ((x - 236) * gx_length / 596.0) - (gx_length / 2)
		y = ((y - 193) * gy_length / 447.0) - (gy_length / 2)
		
		if self.modes[self.selected_mode] == 'Add':
			if self.choices[self.selected_choice] == 'Source':
				sources.append(Source(self.current_strength, x, y))
			elif self.choices[self.selected_choice] == 'Sink':
				sources.append(Source(-self.current_strength, x, y))
			elif self.choices[self.selected_choice] == 'Doublet':
				sources.append(Doublet(self.current_strength, x, y))
			elif self.choices[self.selected_choice] == 'Vortex':
				sources.append(Vortex(self.current_strength, x, y))
		elif self.modes[self.selected_mode] == 'Inspect':
			iu, iv = locate_velocity_values(x, y, self.u, self.v)
			
			ix = str(round(x, 3))
			iy = str(round(y, 3))
			iu = str(round(iu, 3))
			iv = str(round(iv, 3))
			self.inspect_label.text = '(' + ix + ', ' + iy + ') <' + iu + ', ' + iv + '>'

		self.u, self.v = calculate_fluid()
		self.refresh_graph()

	def cycle_next(self):
		self.selected_choice = (self.selected_choice + 1) % len(self.choices)
		self.choice_label.text = 'Selected: ' + self.choices[self.selected_choice]

	def cycle_prev(self):
		self.selected_choice = (self.selected_choice - 1) % len(self.choices)
		self.choice_label.text = 'Selected: ' + self.choices[self.selected_choice]

	def change_strength(self, change):
		self.current_strength = self.current_strength + change
		self.strength_label.text = 'Strength: ' + str(self.current_strength)

	def clear_components(self):
		plt.close()
		sources.clear()
		sources.append(Doublet((0.25**2) * 2 * np.pi, 0, 0.5))
		sources.append(Doublet((0.25**2) * 2 * np.pi, 0, -0.5)) 
		# change this for precise stuff ^^
		self.u, self.v = calculate_fluid()
		self.refresh_graph()
	
	def change_mode(self): # the important thing is to find balls
		self.selected_mode = (self.selected_mode + 1) % len(self.modes)
		self.mode_label.text = 'Mode: ' + self.modes[self.selected_mode]
		
	def set_sources(self, new_sources):
		self.sources = new_sources


thescene = TheScene()

root = KBHandler(scene_input=thescene)
root.present('fullscreen', hide_title_bar=True)

thescene.clear_components()

