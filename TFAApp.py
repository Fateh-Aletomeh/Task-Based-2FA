from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import requests
import json
import time
import hmac
import hashlib
import base64
import os
import random

# Set app colors
PRIMARY_COLOR = "#4A86E8"  # Blue
SECONDARY_COLOR = "#FFFFFF"  # White
BACKGROUND_COLOR = "#F5F5F5"  # Light gray
TEXT_COLOR = "#333333"  # Dark gray
SUCCESS_COLOR = "#4CAF50"  # Green
ERROR_COLOR = "#F44336"  # Red

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Add app logo
        logo = Image(source='Graphics/Logo.png', size_hint=(1, 0.3))
        self.layout.add_widget(logo)
        
        # Add welcome text
        self.welcome_label = Label(
            text="[b]Task-Based 2FA Authentication[/b]",
            color=get_color_from_hex(TEXT_COLOR),
            size_hint=(1, 0.2),
            markup = True
        )
        self.layout.add_widget(self.welcome_label)
        
        # Add info text
        self.info_label = Label(
            text="Complete the task shown here on your desktop browser to authenticate",
            color=get_color_from_hex(TEXT_COLOR),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle',
            text_size=(Window.width - 40, None)
        )
        self.layout.add_widget(self.info_label)
        
        # Adjust font size dynamically
        self.bind(size=self.update_font_sizes)
        
        # Add fetch task button
        self.fetch_button = Button(
            text="Fetch Authentication Task",
            background_color=get_color_from_hex(PRIMARY_COLOR),
            color=get_color_from_hex(SECONDARY_COLOR),
            size_hint=(1, 0.15),
            pos_hint={'center_x': 0.5}
        )
        self.fetch_button.bind(on_press=self.fetch_task)
        self.layout.add_widget(self.fetch_button)
        
        self.add_widget(self.layout)

    def update_font_sizes(self, *args):
        self.welcome_label.font_size = self.width * 0.07  # Scale based on screen width
        self.info_label.font_size = self.width * 0.05
        self.info_label.text_size = (self.width - 40, None)  # Ensure it wraps properly

    
    def fetch_task(self, instance):
        # Load task data from JSON file
        try:
            with open('sample_task_with_named_colors.json', 'r') as file:
                task_data = json.load(file)
                self.manager.get_screen('task').set_task_data(task_data)
                self.manager.current = 'task'
        except Exception as e:
            print(f"Error loading task data: {e}")

class StaticCircleWidget(Image):
    def __init__(self, circle_id, color, is_correct, **kwargs):
        super(StaticCircleWidget, self).__init__(**kwargs)
        self.circle_id = circle_id
        self.color = color
        # Use highlighted image for correct circles, regular image for others
        if is_correct:
            self.source = f"Graphics/highlighted_{color}_circle.png"
        else:
            self.source = f"Graphics/{color}_circle.png"
        self.size_hint = (None, None)
        self.size = (80, 80)  # Slightly smaller size for grid layout
        
        # Get the circle number for display
        self.circle_number = circle_id.split('-')[1]

class BackgroundImage(Image):
    def __init__(self, **kwargs):
        super(BackgroundImage, self).__init__(**kwargs)
        # Use fit mode to properly scale the image
        self.fit_mode = "contain"

class TaskScreen(Screen):
    def __init__(self, **kwargs):
        super(TaskScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Add header
        header_label = Label(
            text="Authentication Task",
            font_size=40,
            color=get_color_from_hex(TEXT_COLOR),
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(header_label)
        
    
        
        # Create a FloatLayout container for background and grid
        self.task_container = FloatLayout(size_hint=(1, 0.5))
        
        # Add background image using custom class
        self.background = BackgroundImage(
            source='Graphics/Task_Background.png',
            fit_mode="fill",  # "fill" scales to fill the container
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.task_container.add_widget(self.background)
        
        # Add grid layout for circles (4x4)
        self.circle_grid = GridLayout(
            cols=4,
            spacing=10,
            size_hint=(None, None),
            width = 350,
            height = 350,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.task_container.add_widget(self.circle_grid)
        
        self.layout.add_widget(self.task_container)
        
        # Add answer display
        self.answer_label = Label(
            text="Correct circles are highlighted",
            font_size=30,
            color=get_color_from_hex(SUCCESS_COLOR),
            size_hint=(1, 0.1),
            halign='center',
            valign='middle',
            text_size=(Window.width - 40, None)
        )
        self.layout.add_widget(self.answer_label)
        
        # Add timer
        self.timer_label = Label(
            text="Time remaining: 5:00",
            font_size=30,
            color=get_color_from_hex(ERROR_COLOR),
            size_hint=(1, 0.05)
        )
        self.layout.add_widget(self.timer_label)
        
        # Add buttons at the bottom
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        cancel_button = Button(
            text="Cancel",
            background_color=get_color_from_hex(ERROR_COLOR),
            color=get_color_from_hex(SECONDARY_COLOR),
            size_hint=(0.5, 0.8),
            pos_hint={'center_y': 0.5}
        )
        cancel_button.bind(on_press=self.cancel_auth)
        buttons_layout.add_widget(cancel_button)
        
        refresh_button = Button(
            text="Refresh Task",
            background_color=get_color_from_hex(PRIMARY_COLOR),
            color=get_color_from_hex(SECONDARY_COLOR),
            size_hint=(0.5, 0.8),
            pos_hint={'center_y': 0.5}
        )
        refresh_button.bind(on_press=self.refresh_task)
        buttons_layout.add_widget(refresh_button)
        
        self.layout.add_widget(buttons_layout)
        
        self.add_widget(self.layout)
        
        self.remaining_time = 300  # 5 minutes in seconds
        self.timer_event = None
        self.task_data = None
        self.circle_widgets = []
    
    def set_task(self, task_text):
        # Start the timer when task is set
        self.remaining_time = 300
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def set_task_data(self, task_data):
        self.task_data = task_data

        
        # Get the expected response (correct circles)
        expected_response = task_data.get('expectedResponse', [])
        
        # Clear previous circles
        self.circle_grid.clear_widgets()
        self.circle_widgets = []
        
        # Create circle widgets based on JSON data
        for circle in task_data.get('circles', []):
            circle_id = circle.get('id')
            color = circle.get('color')
            
            # Check if this circle is in the expected response (correct answer)
            is_correct = circle_id in expected_response
            
            circle_widget = StaticCircleWidget(circle_id, color, is_correct)
            self.circle_widgets.append(circle_widget)
            self.circle_grid.add_widget(circle_widget)
        
        # Add empty cells to complete the 4x4 grid (if needed)
        remaining_cells = 16 - len(task_data.get('circles', []))
        for _ in range(remaining_cells):
            empty_space = BoxLayout()
            self.circle_grid.add_widget(empty_space)
        
    
        
        # Start the timer
        self.remaining_time = 300
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.text = f"Time remaining: {minutes}:{seconds:02d}"
        
        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.timer_label.text = "Time expired"

    
    def cancel_auth(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.current = 'login'
    
    def refresh_task(self, instance):
        # In a real app, this would fetch a new task from the backend
        # For demo, we'll reload the same task or generate a new one
        try:
            with open('sample_task_with_named_colors.json', 'r') as file:
                task_data = json.load(file)
                self.set_task_data(task_data)
        except Exception as e:
            print(f"Error loading task data: {e}")


class AuthApp(App):
    def build(self):
        # Set window background color
        Window.clearcolor = get_color_from_hex(BACKGROUND_COLOR)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(TaskScreen(name='task'))
        
        return sm


if __name__ == '__main__':
    AuthApp().run()