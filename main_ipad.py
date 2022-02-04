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


calculate_fluid()

img = ui.Image.named('result.png')


class TheScene(Scene):
	def setup(self):

		self.current_strength = DEFAULT_STRENGTH
		self.selected_choice = 0
		self.choices = ['Source', 'Sink', 'Doublet', 'Vortex']

		self.graphimage = SpriteNode(Texture(img), scale=0.5)
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

		if self.choices[self.selected_choice] == 'Source':
			sources.append(Source(self.current_strength, x, y))
		elif self.choices[self.selected_choice] == 'Sink':
			sources.append(Source(-self.current_strength, x, y))
		elif self.choices[self.selected_choice] == 'Doublet':
			sources.append(Doublet(self.current_strength, x, y))
		elif self.choices[self.selected_choice] == 'Vortex':
			sources.append(Vortex(self.current_strength, x, y))

		calculate_fluid()
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
		sources.clear()
		sources.append(Source(0, 0, 0))
		calculate_fluid()
		self.refresh_graph()


root = KBHandler(scene_input=TheScene())
root.present('fullscreen', hide_title_bar=True)

