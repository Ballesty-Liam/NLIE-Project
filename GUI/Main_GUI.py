import tkinter as tk
from tkinter import ttk, messagebox
import json
from api_handler import APIHandler
from datetime import datetime


class SelectionFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a styled frame
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f0f0f0')
        self.configure(style='Custom.TFrame', padding="20")

        # Title
        title_label = ttk.Label(self,
                                text="LLM Analysis Tool",
                                font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)

        # API Selection
        api_frame = ttk.LabelFrame(self, text="Select API", padding="10")
        api_frame.pack(fill='x', padx=20, pady=10)

        self.api_var = tk.StringVar()
        apis = ['Claude', 'ChatGPT', 'Sonar', 'xAI']
        for api in apis:
            ttk.Radiobutton(api_frame,
                            text=api,
                            variable=self.api_var,
                            value=api).pack(anchor='w', pady=5)

        # Analysis Type Selection
        analysis_frame = ttk.LabelFrame(self, text="Select Analysis Type", padding="10")
        analysis_frame.pack(fill='x', padx=20, pady=10)

        self.analysis_var = tk.StringVar()
        analysis_types = [
            'Sentiment Analysis',
            'Named Entity Recognition',
            'Text Classification'
        ]
        for analysis_type in analysis_types:
            ttk.Radiobutton(analysis_frame,
                            text=analysis_type,
                            variable=self.analysis_var,
                            value=analysis_type).pack(anchor='w', pady=5)

        # Continue Button
        continue_btn = ttk.Button(self,
                                  text="Continue",
                                  command=self.validate_and_continue)
        continue_btn.pack(pady=20)

    def validate_and_continue(self):
        if not self.api_var.get() or not self.analysis_var.get():
            messagebox.showwarning(
                "Selection Required",
                "Please select both an API and an analysis type."
            )
            return

        self.controller.selected_api = self.api_var.get()
        self.controller.selected_analysis = self.analysis_var.get()
        self.controller.show_input_frame()


class InputFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding="20")

        # Title showing selected options
        self.title_label = ttk.Label(self,
                                     text="",
                                     font=('Helvetica', 12))
        self.title_label.pack(pady=10)

        # Input area
        input_label = ttk.Label(self,
                                text="Enter text for analysis:",
                                font=('Helvetica', 10))
        input_label.pack(anchor='w', pady=(10, 5))

        self.text_input = tk.Text(self, height=10, width=50)
        self.text_input.pack(pady=10, fill='both', expand=True)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', pady=10)

        back_btn = ttk.Button(button_frame,
                              text="Back",
                              command=self.controller.show_selection_frame)
        back_btn.pack(side='left', padx=5)

        analyze_btn = ttk.Button(button_frame,
                                 text="Analyze",
                                 command=self.analyze)
        analyze_btn.pack(side='right', padx=5)

    def update_title(self):
        self.title_label.config(
            text=f"API: {self.controller.selected_api} | "
                 f"Analysis: {self.controller.selected_analysis}"
        )

    def analyze(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning(
                "Input Required",
                "Please enter text for analysis."
            )
            return

        try:
            result = self.controller.api_handler.analyze(
                self.controller.selected_api,
                self.controller.selected_analysis,
                text
            )

            # Add metadata to results
            self.controller.analysis_results = {
                "api": self.controller.selected_api,
                "analysis_type": self.controller.selected_analysis,
                "input_text": text,
                "results": result
            }

            self.controller.show_results_frame()

        except Exception as e:
            messagebox.showerror(
                "Analysis Error",
                f"An error occurred during analysis: {str(e)}"
            )


class ResultsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding="20")

        # Title
        self.title_label = ttk.Label(self,
                                     text="Analysis Results",
                                     font=('Helvetica', 14, 'bold'))
        self.title_label.pack(pady=10)

        # Results text area
        self.results_text = tk.Text(self, height=15, width=60)
        self.results_text.pack(pady=10, fill='both', expand=True)

        # Visualization frame (placeholder)
        self.viz_frame = ttk.Frame(self)
        self.viz_frame.pack(fill='both', expand=True, pady=10)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', pady=10)

        new_analysis_btn = ttk.Button(button_frame,
                                      text="New Analysis",
                                      command=self.controller.show_selection_frame)
        new_analysis_btn.pack(side='left', padx=5)

        download_btn = ttk.Button(button_frame,
                                  text="Download Results",
                                  command=self.save_results)
        download_btn.pack(side='right', padx=5)

    def display_results(self, results):
        # Clear previous results
        self.results_text.delete("1.0", "end")

        # Display formatted results
        formatted_results = json.dumps(results, indent=2)
        self.results_text.insert("1.0", formatted_results)

    def save_results(self):
        # We'll implement the save functionality later
        messagebox.showinfo(
            "Save Results",
            "Save functionality will be implemented soon!"
        )


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("LLM Analysis Tool")
        self.geometry("800x600")

        # Initialize API handler
        self.api_handler = APIHandler()

        # Initialize variables
        self.selected_api = None
        self.selected_analysis = None
        self.analysis_results = None

        # Create frames
        self.selection_frame = SelectionFrame(self, self)
        self.input_frame = InputFrame(self, self)
        self.results_frame = ResultsFrame(self, self)

        # Start with selection frame
        self.show_selection_frame()

    def show_selection_frame(self):
        self.input_frame.pack_forget()
        self.results_frame.pack_forget()
        self.selection_frame.pack(fill='both', expand=True)

    def show_input_frame(self):
        self.selection_frame.pack_forget()
        self.results_frame.pack_forget()
        self.input_frame.pack(fill='both', expand=True)
        self.input_frame.update_title()

    def show_results_frame(self):
        self.selection_frame.pack_forget()
        self.input_frame.pack_forget()
        self.results_frame.pack(fill='both', expand=True)
        self.results_frame.display_results(self.analysis_results)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()