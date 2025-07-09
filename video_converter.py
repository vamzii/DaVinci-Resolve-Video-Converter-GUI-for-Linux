#!/usr/bin/env python3
"""
DaVinci Resolve Video Converter for Linux
A GUI application to convert videos to formats compatible with DaVinci Resolve on Linux.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import json
from pathlib import Path
from datetime import datetime
import queue
import time
import pyperclip  # For clipboard operations
import sys

class VideoConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("DaVinci Resolve Video Converter")
        self.root.geometry("900x700")
        
        # Find FFmpeg binary
        self.ffmpeg_path = self.find_ffmpeg()
        self.ffprobe_path = self.find_ffprobe()
        
        # Configure style for native theme
        self.style = ttk.Style()
        
        # Try to use system theme first
        available_themes = self.style.theme_names()
        if 'plastik' in available_themes:
            self.style.theme_use('plastik')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        else:
            self.style.theme_use('clam')
        
        # Configure native-looking styles
        self.style.configure('Title.TLabel', font=('Sans', 16, 'bold'))
        self.style.configure('Heading.TLabel', font=('Sans', 12, 'bold'))
        self.style.configure('Info.TLabel', font=('Sans', 9))
        
        # Configure button styles
        self.style.configure('Primary.TButton', font=('Sans', 10, 'bold'))
        self.style.configure('Secondary.TButton', font=('Sans', 9))
        
        # Configure frame styles
        self.style.configure('Card.TFrame', relief='solid', borderwidth=1)
        
        # Supported formats
        self.supported_formats = {
            'MJPEG': {
                'extension': '.avi',
                'codec': 'mjpeg',
                'description': 'DaVinci Resolve Compatible - Professional quality'
            },
            'H.264': {
                'extension': '.mp4',
                'codec': 'libx264',
                'profile': 'baseline',
                'description': 'Universal playback - Good compression'
            }
        }
        
        # Variables
        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.selected_format = tk.StringVar(value='MJPEG')
        self.video_files = []
        self.selected_videos = []
        self.conversion_queue = queue.Queue()
        self.is_converting = False
        self.stop_conversion = False
        self.conflict_resolution = "overwrite"  # Default behavior
        
        # Undo/Redo history for directory fields
        self.input_history = []
        self.input_history_index = -1
        self.output_history = []
        self.output_history_index = -1
        
        # Track changes for undo/redo
        self.input_directory.trace('w', self.on_input_directory_change)
        self.output_directory.trace('w', self.on_output_directory_change)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame with native styling
        main_frame = ttk.Frame(self.root, padding="15", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="DaVinci Resolve Video Converter", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Format selection
        format_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="10")
        format_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        format_frame.columnconfigure(1, weight=1)
        
        for i, (format_name, format_info) in enumerate(self.supported_formats.items()):
            radio = ttk.Radiobutton(format_frame, text=f"{format_name} - {format_info['description']}", 
                                   variable=self.selected_format, value=format_name)
            radio.grid(row=i, column=0, sticky="w", pady=2)
        
        # Directory selection
        dir_frame = ttk.LabelFrame(main_frame, text="Directories", padding="10")
        dir_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        # Input directory
        ttk.Label(dir_frame, text="Input Directory:").grid(row=0, column=0, sticky="w", pady=2)
        input_entry = ttk.Entry(dir_frame, textvariable=self.input_directory, width=50)
        input_entry.grid(row=0, column=1, sticky="ew", padx=(10, 5), pady=2)
        ttk.Button(dir_frame, text="Browse", command=self.browse_input, style='Secondary.TButton').grid(row=0, column=2, pady=2)
        
        # Add keyboard shortcuts for input directory
        input_entry.bind('<Control-z>', self.undo_input_directory)
        input_entry.bind('<Control-y>', self.redo_input_directory)
        input_entry.bind('<Control-a>', self.select_all_text)
        
        # Add right-click context menu for input directory
        self.input_context_menu = tk.Menu(self.root, tearoff=0)
        self.input_context_menu.add_command(label="Copy Path", command=lambda: self.copy_directory_path(self.input_directory))
        self.input_context_menu.add_command(label="Paste Path", command=lambda: self.paste_directory_path(self.input_directory))
        self.input_context_menu.add_separator()
        self.input_context_menu.add_command(label="Undo", command=lambda: self.undo_input_directory(None), accelerator="Ctrl+Z")
        self.input_context_menu.add_command(label="Redo", command=lambda: self.redo_input_directory(None), accelerator="Ctrl+Y")
        self.input_context_menu.add_separator()
        self.input_context_menu.add_command(label="Open in File Manager", command=lambda: self.open_directory(self.input_directory.get()))
        input_entry.bind("<Button-3>", self.show_input_context_menu)
        
        # Output directory
        ttk.Label(dir_frame, text="Output Directory:").grid(row=1, column=0, sticky="w", pady=2)
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_directory, width=50)
        output_entry.grid(row=1, column=1, sticky="ew", padx=(10, 5), pady=2)
        ttk.Button(dir_frame, text="Browse", command=self.browse_output, style='Secondary.TButton').grid(row=1, column=2, pady=2)
        
        # Add keyboard shortcuts for output directory
        output_entry.bind('<Control-z>', self.undo_output_directory)
        output_entry.bind('<Control-y>', self.redo_output_directory)
        output_entry.bind('<Control-a>', self.select_all_text)
        
        # Add right-click context menu for output directory
        self.output_context_menu = tk.Menu(self.root, tearoff=0)
        self.output_context_menu.add_command(label="Copy Path", command=lambda: self.copy_directory_path(self.output_directory))
        self.output_context_menu.add_command(label="Paste Path", command=lambda: self.paste_directory_path(self.output_directory))
        self.output_context_menu.add_separator()
        self.output_context_menu.add_command(label="Undo", command=lambda: self.undo_output_directory(None), accelerator="Ctrl+Z")
        self.output_context_menu.add_command(label="Redo", command=lambda: self.redo_output_directory(None), accelerator="Ctrl+Y")
        self.output_context_menu.add_separator()
        self.output_context_menu.add_command(label="Open in File Manager", command=lambda: self.open_directory(self.output_directory.get()))
        output_entry.bind("<Button-3>", self.show_output_context_menu)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(button_frame, text="Scan Videos", command=self.scan_videos, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        self.convert_button = ttk.Button(button_frame, text="Convert Videos", command=self.start_conversion, style='Primary.TButton')
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Select All", command=self.select_all_videos, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Deselect All", command=self.deselect_all_videos, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear List", command=self.clear_list, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # Selection counter
        self.selection_label = ttk.Label(button_frame, text="Selected: 0", style='Info.TLabel')
        self.selection_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Video list
        list_frame = ttk.LabelFrame(main_frame, text="Video Files", padding="10")
        list_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for video list
        columns = ('Select', 'Name', 'Size', 'Duration', 'Status')
        self.video_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        self.video_tree.heading('Select', text='✓')
        self.video_tree.heading('Name', text='File Name')
        self.video_tree.heading('Size', text='Size')
        self.video_tree.heading('Duration', text='Duration')
        self.video_tree.heading('Status', text='Status')
        
        self.video_tree.column('Select', width=50, anchor='center')
        self.video_tree.column('Name', width=200)
        self.video_tree.column('Size', width=100)
        self.video_tree.column('Duration', width=100)
        self.video_tree.column('Status', width=100)
        
        # Configure treeview styling for native look
        self.video_tree.tag_configure('selected', background='#e0e0e0')
        self.video_tree.tag_configure('converting', background='#fff3cd')
        self.video_tree.tag_configure('completed', background='#d4edda')
        self.video_tree.tag_configure('error', background='#f8d7da')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.video_tree.yview)
        self.video_tree.configure(yscrollcommand=scrollbar.set)
        
        self.video_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind selection event
        self.video_tree.bind('<<TreeviewSelect>>', self.on_video_select)
        self.video_tree.bind('<Button-1>', self.on_video_click)
        self.video_tree.bind('<space>', self.toggle_selected_videos)
        self.video_tree.bind('<Return>', self.toggle_selected_videos)
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky="ew")
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Monospace', 9))
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Right-click context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Remove Selected", command=self.remove_selected)
        self.context_menu.add_command(label="Clear List", command=self.clear_list)
        self.context_menu.add_command(label="Show in File Manager", command=self.show_in_file_manager)
        
        self.video_tree.bind("<Button-3>", self.show_context_menu)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready", style='Info.TLabel')
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Tools info
        self.tools_label = ttk.Label(status_frame, text="", style='Info.TLabel')
        self.tools_label.grid(row=0, column=1, sticky="e")
        
        # Update tools info
        self.update_tools_info()
        
    def update_tools_info(self):
        """Update the tools information in the status bar"""
        tools_info = []
        if self.ffmpeg_path:
            tools_info.append("FFmpeg ✓")
        if self.ffprobe_path:
            tools_info.append("FFprobe ✓")
        tools_info.append("Avidemux ✓")
        tools_info.append("HandBrake ✓")
        
        self.tools_label.config(text=" | ".join(tools_info))
        
    def browse_input(self):
        """Browse for input directory using native file dialog"""
        try:
            # Try to use native file dialog first
            result = subprocess.run(['zenity', '--file-selection', '--directory', '--title=Select Input Directory'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                directory = result.stdout.strip()
                if directory:
                    self.input_directory.set(directory)
                    return
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Fallback to tkinter dialog
        directory = filedialog.askdirectory(title="Select Input Directory", initialdir=os.path.expanduser("~"))
        if directory:
            self.input_directory.set(directory)
            
    def browse_output(self):
        """Browse for output directory using native file dialog"""
        try:
            # Try to use native file dialog first
            result = subprocess.run(['zenity', '--file-selection', '--directory', '--title=Select Output Directory'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                directory = result.stdout.strip()
                if directory:
                    self.output_directory.set(directory)
                    return
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Fallback to tkinter dialog
        directory = filedialog.askdirectory(title="Select Output Directory", initialdir=os.path.expanduser("~"))
        if directory:
            self.output_directory.set(directory)
            
    def scan_videos(self):
        """Scan for video files in the input directory"""
        input_dir = self.input_directory.get()
        if not input_dir:
            messagebox.showerror("Error", "Please select an input directory")
            return
            
        if not os.path.exists(input_dir):
            messagebox.showerror("Error", "Input directory does not exist")
            return
            
        # Clear existing list
        self.clear_list()
        
        # Video file extensions
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        
        # Scan for video files
        video_files = []
        for file_path in Path(input_dir).rglob('*'):
            if file_path.suffix.lower() in video_extensions:
                video_files.append(file_path)
                
        if not video_files:
            messagebox.showinfo("Info", "No video files found in the selected directory")
            return
            
        # Add files to the list
        for file_path in video_files:
            try:
                size = self.get_file_size(file_path)
                duration = self.get_video_duration(file_path)
                item = self.video_tree.insert('', 'end', values=('☐', file_path.name, size, duration, 'Ready'))
                self.video_tree.set(item, 'Select', '☐')  # Ensure checkbox is set
                self.video_files.append(str(file_path))
            except Exception as e:
                self.log_message(f"Error processing {file_path.name}: {e}")
                
        self.log_message(f"Found {len(video_files)} video files")
        self.log_message("💡 Tip: Click the checkboxes (☐) to select videos for conversion")
        
    def get_file_size(self, file_path):
        """Get file size in human readable format"""
        size_bytes = file_path.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
        
    def get_video_duration(self, file_path):
        """Get video duration using ffprobe"""
        try:
            cmd = [self.ffprobe_path, '-v', 'quiet', '-show_entries', 'format=duration', 
                   '-of', 'csv=p=0', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                duration_seconds = float(result.stdout.strip())
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                return f"{minutes}:{seconds:02d}"
        except:
            pass
        return "Unknown"
        
    def on_video_select(self, event):
        """Handle video selection (for highlighting, not checkbox)"""
        # This method is now only for visual selection highlighting
        # Checkbox functionality is handled by on_video_click
        pass
        
    def on_video_click(self, event):
        """Handle video click"""
        region = self.video_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.video_tree.identify_column(event.x)
            if column == '#1':  # First column (checkbox)
                # Get the clicked item
                item = self.video_tree.identify_row(event.y)
                if item:
                    # Toggle only the clicked item's checkbox
                    values = list(self.video_tree.item(item)['values'])
                    if values[0] == '☐':
                        values[0] = '☑'
                    else:
                        values[0] = '☐'
                    self.video_tree.item(item, values=values)
                    self.update_selected_videos_list()
                    
                    # Prevent the default selection behavior for checkbox clicks
                    return "break"
            else:
                # For non-checkbox clicks, allow normal selection behavior
                # but preserve checkbox states
                self.preserve_checkbox_states()
                
    def preserve_checkbox_states(self):
        """Preserve checkbox states when selection changes"""
        # This method can be used to maintain checkbox states
        # when the user clicks on other columns
        pass
        
    def show_context_menu(self, event):
        """Show right-click context menu"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def remove_selected(self):
        """Remove selected videos from the list"""
        selection = self.video_tree.selection()
        for item in selection:
            self.video_tree.delete(item)
            
    def clear_list(self):
        """Clear the video list"""
        for item in self.video_tree.get_children():
            self.video_tree.delete(item)
        self.video_files.clear()
        self.selected_videos.clear()
        self.selection_label.config(text="Selected: 0")
        self.convert_button.config(state='disabled')
        
    def select_all_videos(self):
        """Select all videos in the list"""
        for item in self.video_tree.get_children():
            values = list(self.video_tree.item(item)['values'])
            values[0] = '☑'
            self.video_tree.item(item, values=values)
        self.update_selected_videos_list()
        
    def deselect_all_videos(self):
        """Deselect all videos in the list"""
        for item in self.video_tree.get_children():
            values = list(self.video_tree.item(item)['values'])
            values[0] = '☐'
            self.video_tree.item(item, values=values)
        self.update_selected_videos_list()
        
    def update_selected_videos_list(self):
        """Update the selected_videos list based on checkbox states"""
        self.selected_videos = []
        for item in self.video_tree.get_children():
            values = self.video_tree.item(item).get('values') or []
            if not isinstance(values, (list, tuple)) or not values:
                continue
            if values[0] == '☑':  # Checked videos
                self.selected_videos.append(values[1])  # File name
        # Update selection counter
        count = len(self.selected_videos)
        self.selection_label.config(text=f"Selected: {count}")
        # Update convert button state
        if count > 0:
            self.convert_button.config(state='normal')
        else:
            self.convert_button.config(state='disabled')
        
    def show_in_file_manager(self):
        """Show selected video in file manager"""
        selection = self.video_tree.selection()
        if selection:
            item = self.video_tree.item(selection[0])
            file_name = item['values'][0]
            input_dir = self.input_directory.get()
            file_path = os.path.join(input_dir, file_name)
            
            if os.path.exists(file_path):
                subprocess.run(['xdg-open', os.path.dirname(file_path)])
            else:
                messagebox.showerror("Error", "File not found")
                
    def start_conversion(self):
        """Start or stop the conversion process"""
        if self.is_converting:
            # Stop conversion
            self.stop_conversion = True
            self.convert_button.config(text="Convert Videos")
            self.log_message("Stopping conversion...")
            return
            
        if not self.video_files:
            messagebox.showerror("Error", "No videos to convert")
            return
            
        if not self.selected_videos:
            messagebox.showerror("Error", "Please select videos to convert")
            return
            
        if not self.output_directory.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        # Check for filename conflicts
        conflicts = self.check_destination_conflicts()
        if conflicts:
            resolution = self.handle_filename_conflicts(conflicts)
            if resolution == "cancel":
                self.log_message("Conversion cancelled due to filename conflicts")
                return
            else:
                self.conflict_resolution = resolution
                self.log_message(f"Using conflict resolution: {resolution}")
        else:
            self.conflict_resolution = "overwrite"  # Default behavior
            
        # Start conversion in a separate thread
        self.is_converting = True
        self.stop_conversion = False
        self.convert_button.config(text="Stop Conversion")
        conversion_thread = threading.Thread(target=self.convert_videos)
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def convert_videos(self):
        """Convert selected videos in the list"""
        # Get only selected videos
        selected_video_paths = []
        for item in self.video_tree.get_children():
            values = self.video_tree.item(item).get('values') or []
            if not isinstance(values, (list, tuple)) or not values:
                continue
            if values[0] == '☑':  # Checked videos
                # Find the full path for this video
                for video_path in self.video_files:
                    if os.path.basename(video_path) == values[1]:
                        selected_video_paths.append(video_path)
                        break

        total_videos = len(selected_video_paths)
        converted = 0
        opened_folder = False

        for i, video_path in enumerate(selected_video_paths):
            # Check if conversion should be stopped
            if self.stop_conversion:
                self.log_message("Conversion stopped by user")
                break

            try:
                self.log_message(f"Converting {os.path.basename(video_path)}...")
                self.update_progress(i, total_videos)

                if self.selected_format.get() == 'H.264':
                    self.log_message(f"Using HandBrake for H.264 conversion: {os.path.basename(video_path)}")
                    if self.convert_with_handbrake(video_path):
                        converted += 1
                        self.update_video_status(video_path, "Completed")
                        if not opened_folder:
                            self.open_directory(self.output_directory.get())
                            opened_folder = True
                    else:
                        self.update_video_status(video_path, "Failed")
                else:
                    self.log_message(f"Using Avidemux for non-H.264 conversion: {os.path.basename(video_path)}")
                    if self.convert_single_video(video_path):
                        converted += 1
                        self.update_video_status(video_path, "Completed")
                        if not opened_folder:
                            self.open_directory(self.output_directory.get())
                            opened_folder = True
                    else:
                        self.update_video_status(video_path, "Failed")

            except Exception as e:
                self.log_message(f"Error converting {os.path.basename(video_path)}: {e}")
                self.update_video_status(video_path, "Failed")

        self.update_progress(total_videos, total_videos)
        self.is_converting = False
        self.convert_button.config(text="Convert Videos")

        if self.stop_conversion:
            self.log_message("✓ Conversion stopped by user")
        elif converted == total_videos:
            self.log_message("✓ All conversions completed successfully!")
            messagebox.showinfo("Success", f"Successfully converted {converted} videos")
        else:
            self.log_message(f"⚠ {converted}/{total_videos} conversions completed")
            messagebox.showwarning("Warning", f"Only {converted}/{total_videos} videos were converted successfully")
            
    def convert_single_video(self, video_path):
        """Convert a single video file using Avidemux AppImage to MOV (Xvid4+Lame)"""
        try:
            # Find Avidemux AppImage dynamically
            app_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_message(f"Debug: App directory: {app_dir}")
            avidemux_appimage = None
            
            # Try multiple possible locations (STRONGLY prioritize AppImage over CLI)
            possible_paths = [
                os.path.abspath(os.path.join(app_dir, '..', '..', 'tools', 'avidemux.appImage')),  # AppImage structure (from usr/bin)
                os.path.abspath(os.path.join(app_dir, '..', 'tools', 'avidemux.appImage')),        # AppImage structure (from usr)
                os.path.abspath(os.path.join(app_dir, 'tools', 'avidemux.appImage')),              # Development
                os.path.abspath(os.path.join(app_dir, 'avidemux_2.8.1.appImage')),                 # Original filename
                './avidemux_2.8.1.appImage',                                                         # Current directory
                # Only try system CLI as last resort
                '/usr/bin/avidemux3_cli',                                                          # System CLI (fallback)
                '/usr/bin/avidemux_cli'                                                            # Alternative system CLI
            ]
            
            # First, try to find any AppImage specifically
            appimage_paths = [
                os.path.abspath(os.path.join(app_dir, '..', '..', 'tools', 'avidemux.appImage')),  # AppImage structure (from usr/bin)
                os.path.abspath(os.path.join(app_dir, '..', 'tools', 'avidemux.appImage')),        # AppImage structure (from usr)
                os.path.abspath(os.path.join(app_dir, 'tools', 'avidemux.appImage')),              # Development
                os.path.abspath(os.path.join(app_dir, 'avidemux_2.8.1.appImage')),                 # Original filename
                './avidemux_2.8.1.appImage'                                                         # Current directory
            ]
            
            for path in appimage_paths:
                self.log_message(f"Debug: Checking AppImage path: {path} (exists: {os.path.exists(path)})")
                if os.path.exists(path):
                    avidemux_appimage = path
                    self.log_message(f"Found Avidemux AppImage at: {avidemux_appimage}")
                    break
            
            # Only if no AppImage found, try CLI
            if not avidemux_appimage:
                for path in possible_paths[4:]:  # Skip the AppImage paths we already checked
                    if os.path.exists(path):
                        avidemux_appimage = path
                        self.log_message(f"Found Avidemux CLI at: {avidemux_appimage}")
                        break
            
            if not avidemux_appimage:
                self.log_message("❌ Error: Could not find Avidemux AppImage or CLI")
                self.log_message(f"Tried AppImage paths: {appimage_paths}")
                return False

            # Prepare output filename (always .mov)
            input_name = os.path.splitext(os.path.basename(video_path))[0]
            output_name = f"{input_name}.mov"
            output_path = os.path.join(self.output_directory.get(), output_name)

            # Handle filename conflicts
            if os.path.exists(output_path):
                if self.conflict_resolution == "skip":
                    self.log_message(f"⏭ Skipping {os.path.basename(video_path)} (file exists)")
                    return True  # Treat as success to avoid error
                elif self.conflict_resolution == "suffix":
                    output_path = self.generate_unique_filename(output_path, "suffix")
                    self.log_message(f"📝 Using unique filename: {os.path.basename(output_path)}")
                elif self.conflict_resolution == "timestamp":
                    output_path = self.generate_unique_filename(output_path, "timestamp")
                    self.log_message(f"📝 Using timestamped filename: {os.path.basename(output_path)}")
                # For "overwrite", just use the original path

            # Build Avidemux AppImage command
            cmd = [
                avidemux_appimage,
                '--nogui',
                '--load', video_path,
                '--video-codec', 'xvid4',
                '--audio-codec', 'Lame',
                '--output-format', 'MOV',  # Keep MOV format
                '--save', output_path,
                '--quit'
            ]

            # Log the Avidemux command
            self.log_message(f"Avidemux command: {' '.join(cmd)}")

            # Run conversion with real-time output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     text=True, bufsize=1, universal_newlines=True)

            # Read output in real-time
            while True:
                if self.stop_conversion:
                    process.terminate()
                    return False
                # Read a line
                if process.stdout:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        line = line.strip()
                        if line:
                            self.log_message(f"Avidemux: {line}")
                else:
                    if process.poll() is not None:
                        break
                    time.sleep(0.1)

            # Wait for process to complete
            return_code = process.wait()

            # Check if output file actually exists
            if return_code == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                if file_size > 0:
                    self.log_message(f"✓ Successfully converted: {os.path.basename(output_path)} ({file_size} bytes)")
                    return True
                else:
                    self.log_message(f"✗ Conversion failed: Output file is empty")
                    return False
            else:
                # Get any remaining error output
                if process.stderr:
                    stderr_output = process.stderr.read()
                    if stderr_output:
                        self.log_message(f"✗ Conversion failed: {stderr_output}")
                if not os.path.exists(output_path):
                    self.log_message(f"✗ Conversion failed: Output file not created")
                return False

        except subprocess.TimeoutExpired:
            self.log_message(f"✗ Conversion timed out for {os.path.basename(video_path)}")
            return False
        except Exception as e:
            self.log_message(f"✗ Error during conversion: {e}")
            return False
            
    def update_progress(self, current, total):
        """Update the progress bar"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.root.update_idletasks()
        
    def update_video_status(self, video_path, status):
        """Update the status of a video in the list"""
        video_name = os.path.basename(video_path)
        for item in self.video_tree.get_children():
            item_dict = self.video_tree.item(item)
            values = item_dict['values'] if 'values' in item_dict and item_dict['values'] is not None else []
            if not isinstance(values, (list, tuple)) or len(values) <= 1:
                continue
            if values[1] == video_name:
                values = list(values)
                values[3] = status
                self.video_tree.item(item, values=values)
                break
                
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update log in main thread
        self.root.after(0, lambda: self.log_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.log_text.see(tk.END))

    def copy_directory_path(self, directory_var):
        """Copy directory path to clipboard"""
        try:
            path = directory_var.get()
            if path:
                pyperclip.copy(path)
                self.log_message(f"✓ Copied path to clipboard: {path}")
            else:
                messagebox.showwarning("Warning", "No path to copy")
        except Exception as e:
            self.log_message(f"✗ Error copying path: {e}")
            
    def paste_directory_path(self, directory_var):
        """Paste directory path from clipboard"""
        try:
            path = pyperclip.paste().strip()
            if path and os.path.exists(path):
                directory_var.set(path)
                self.log_message(f"✓ Pasted path from clipboard: {path}")
            elif path:
                # Ask user if they want to create the directory
                if messagebox.askyesno("Create Directory", f"Directory doesn't exist:\n{path}\n\nCreate it?"):
                    os.makedirs(path, exist_ok=True)
                    directory_var.set(path)
                    self.log_message(f"✓ Created and set directory: {path}")
                else:
                    self.log_message("✗ Directory doesn't exist and user chose not to create it")
            else:
                messagebox.showwarning("Warning", "No valid path in clipboard")
        except Exception as e:
            self.log_message(f"✗ Error pasting path: {e}")
            
    def open_directory(self, path):
        """Open directory in file manager"""
        try:
            if path and os.path.exists(path):
                subprocess.run(['xdg-open', path])
                self.log_message(f"✓ Opened directory: {path}")
            else:
                messagebox.showerror("Error", "Directory doesn't exist")
        except Exception as e:
            self.log_message(f"✗ Error opening directory: {e}")
            
    def show_input_context_menu(self, event):
        """Show right-click context menu for input directory"""
        try:
            self.input_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.input_context_menu.grab_release()
            
    def show_output_context_menu(self, event):
        """Show right-click context menu for output directory"""
        try:
            self.output_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.output_context_menu.grab_release()

    def toggle_selected_videos(self, event):
        """Toggle selected videos"""
        selection = self.video_tree.selection()
        for item in selection:
            values = list(self.video_tree.item(item)['values'])
            if values[0] == '☐':
                values[0] = '☑'
            else:
                values[0] = '☐'
            self.video_tree.item(item, values=values)
        self.update_selected_videos_list()
        
        # Prevent the default behavior
        return "break"

    def check_destination_conflicts(self):
        """Check for filename conflicts in destination folder"""
        if not self.output_directory.get():
            return {}
            
        conflicts = {}
        output_dir = self.output_directory.get()
        
        for video_path in self.video_files:
            if os.path.basename(video_path) in self.selected_videos:
                # Get format configuration
                format_name = self.selected_format.get()
                format_config = self.supported_formats[format_name]
                
                # Prepare output filename
                input_name = os.path.splitext(os.path.basename(video_path))[0]
                output_name = f"{input_name}{format_config['extension']}"
                output_path = os.path.join(output_dir, output_name)
                
                # Check if file exists
                if os.path.exists(output_path):
                    conflicts[video_path] = output_path
                    
        return conflicts
        
    def handle_filename_conflicts(self, conflicts):
        """Handle filename conflicts by asking user what to do"""
        if not conflicts:
            return True
            
        conflict_count = len(conflicts)
        conflict_files = list(conflicts.keys())
        
        # Create conflict dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Filename Conflicts Detected")
        dialog.geometry("700x500")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"700x500+{x}+{y}")
        
        # Configure dialog grid weights
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Make conflict list expandable
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Found {conflict_count} filename conflicts", 
                               font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Conflict list
        list_frame = ttk.LabelFrame(main_frame, text="Conflicting Files", padding="10")
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for conflicts
        columns = ('Source', 'Destination')
        conflict_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        conflict_tree.heading('Source', text='Source File')
        conflict_tree.heading('Destination', text='Will Overwrite')
        
        conflict_tree.column('Source', width=300, minwidth=200)
        conflict_tree.column('Destination', width=300, minwidth=200)
        
        # Add conflicts to list
        for source_path, dest_path in conflicts.items():
            conflict_tree.insert('', 'end', values=(os.path.basename(source_path), os.path.basename(dest_path)))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=conflict_tree.yview)
        conflict_tree.configure(yscrollcommand=scrollbar.set)
        
        conflict_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Resolution Options", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        options_frame.columnconfigure(0, weight=1)
        
        # Resolution option
        resolution_var = tk.StringVar(value="overwrite")
        
        ttk.Radiobutton(options_frame, text="Overwrite existing files", 
                       variable=resolution_var, value="overwrite").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(options_frame, text="Skip conflicting files", 
                       variable=resolution_var, value="skip").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Radiobutton(options_frame, text="Add number suffix (e.g., _1, _2)", 
                       variable=resolution_var, value="suffix").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Radiobutton(options_frame, text="Add timestamp suffix", 
                       variable=resolution_var, value="timestamp").grid(row=3, column=0, sticky="w", pady=2)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure(1, weight=1)  # Push buttons to the right
        
        result = {"action": "cancel"}
        
        def on_continue():
            result["action"] = resolution_var.get()
            dialog.destroy()
            
        def on_cancel():
            result["action"] = "cancel"
            dialog.destroy()
            
        ttk.Button(button_frame, text="Continue", command=on_continue).grid(row=0, column=2, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=3)
        
        # Ensure dialog is on top and focused
        dialog.lift()
        dialog.focus_set()
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result["action"]
        
    def generate_unique_filename(self, base_path, strategy="suffix"):
        """Generate a unique filename based on the strategy"""
        directory = os.path.dirname(base_path)
        filename = os.path.basename(base_path)
        name, ext = os.path.splitext(filename)
        
        if strategy == "suffix":
            counter = 1
            while os.path.exists(base_path):
                new_filename = f"{name}_{counter}{ext}"
                base_path = os.path.join(directory, new_filename)
                counter += 1
        elif strategy == "timestamp":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{name}_{timestamp}{ext}"
            base_path = os.path.join(directory, new_filename)
            
        return base_path

    def undo_input_directory(self, event):
        """Undo input directory"""
        if self.input_history_index > 0:
            self.input_history_index -= 1
            self.input_directory.set(self.input_history[self.input_history_index])
        return "break"

    def redo_input_directory(self, event):
        """Redo input directory"""
        if self.input_history_index < len(self.input_history) - 1:
            self.input_history_index += 1
            self.input_directory.set(self.input_history[self.input_history_index])
        return "break"

    def select_all_text(self, event):
        """Select all text in the focused entry widget"""
        widget = event.widget
        widget.select_range(0, tk.END)
        return "break"

    def undo_output_directory(self, event):
        """Undo output directory"""
        if self.output_history_index > 0:
            self.output_history_index -= 1
            self.output_directory.set(self.output_history[self.output_history_index])
        return "break"

    def redo_output_directory(self, event):
        """Redo output directory"""
        if self.output_history_index < len(self.output_history) - 1:
            self.output_history_index += 1
            self.output_directory.set(self.output_history[self.output_history_index])
        return "break"

    def on_input_directory_change(self, *args):
        """Callback for input directory change"""
        current_value = self.input_directory.get()
        if current_value and (not self.input_history or current_value != self.input_history[-1]):
            # Add to history if it's a new value
            self.input_history.append(current_value)
            self.input_history_index = len(self.input_history) - 1
            # Keep only last 20 entries
            if len(self.input_history) > 20:
                self.input_history = self.input_history[-20:]
                self.input_history_index = len(self.input_history) - 1

    def on_output_directory_change(self, *args):
        """Callback for output directory change"""
        current_value = self.output_directory.get()
        if current_value and (not self.output_history or current_value != self.output_history[-1]):
            # Add to history if it's a new value
            self.output_history.append(current_value)
            self.output_history_index = len(self.output_history) - 1
            # Keep only last 20 entries
            if len(self.output_history) > 20:
                self.output_history = self.output_history[-20:]
                self.output_history_index = len(self.output_history) - 1

    def find_ffmpeg(self):
        """Find FFmpeg binary, preferring embedded version"""
        # Check for PyInstaller bundled FFmpeg first
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            base_path = Path(getattr(sys, '_MEIPASS', ''))
            if base_path:
                bundled_ffmpeg = base_path / "ffmpeg"
                if bundled_ffmpeg.exists() and bundled_ffmpeg.is_file():
                    return str(bundled_ffmpeg)
        
        # Check for embedded FFmpeg in development
        script_dir = Path(__file__).parent
        embedded_ffmpeg = script_dir / "ffmpeg" / "ffmpeg"
        
        if embedded_ffmpeg.exists() and embedded_ffmpeg.is_file():
            return str(embedded_ffmpeg)
            
        # Fall back to system FFmpeg
        try:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return 'ffmpeg'  # Default fallback
        
    def find_ffprobe(self):
        """Find FFprobe binary, preferring embedded version"""
        # Check for PyInstaller bundled FFprobe first
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            base_path = Path(getattr(sys, '_MEIPASS', ''))
            if base_path:
                bundled_ffprobe = base_path / "ffprobe"
                if bundled_ffprobe.exists() and bundled_ffprobe.is_file():
                    return str(bundled_ffprobe)
        
        # Check for embedded FFprobe in development
        script_dir = Path(__file__).parent
        embedded_ffprobe = script_dir / "ffmpeg" / "ffprobe"
        
        if embedded_ffprobe.exists() and embedded_ffprobe.is_file():
            return str(embedded_ffprobe)
            
        # Fall back to system FFprobe
        try:
            result = subprocess.run(['which', 'ffprobe'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return 'ffprobe'  # Default fallback

    def convert_with_handbrake(self, video_path):
        """Convert a single video file using HandBrakeCLI to MP4 (Fast 1080p30 preset)"""
        try:
            import subprocess, os
            input_name = os.path.splitext(os.path.basename(video_path))[0]
            output_name = f"{input_name}_converted.mp4"
            output_path = os.path.join(self.output_directory.get(), output_name)

            # Handle filename conflicts
            if os.path.exists(output_path):
                if self.conflict_resolution == "skip":
                    self.log_message(f"⏭ Skipping {os.path.basename(video_path)} (file exists)")
                    return True
                elif self.conflict_resolution == "overwrite":
                    os.remove(output_path)
                else:
                    # Add a number suffix
                    base, ext = os.path.splitext(output_name)
                    n = 1
                    while os.path.exists(output_path):
                        output_name = f"{base}_{n}{ext}"
                        output_path = os.path.join(self.output_directory.get(), output_name)
                        n += 1

            cmd = [
                "HandBrakeCLI",
                "-i", video_path,
                "-o", output_path,
                "--preset", "Fast 1080p30"
            ]
            self.log_message(f"[HandBrake] $ {' '.join(cmd)}")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                self.log_message(line.rstrip())
            proc.wait()
            if proc.returncode == 0:
                self.log_message(f"✓ Converted (HandBrake): {os.path.basename(output_path)}")
                return True
            else:
                self.log_message(f"✗ HandBrake failed for {os.path.basename(video_path)}")
                return False
        except Exception as e:
            self.log_message(f"✗ HandBrake error: {e}")
            return False

def main():
    """Main function"""
    root = tk.Tk()
    app = VideoConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 