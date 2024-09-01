"""Friday UI Main Module."""

# Standard Library
from pathlib import Path
from configparser import ConfigParser

# Third Party Library
import customtkinter

# Project Library
from friday.main import Friday
from friday.sdk.generation import FridayGenerationError


class FridayUIConstants:
    """Friday AI Personal Assistant User Interface Constants."""

    # Friday UI Configs
    __friday_config_dir = Path(__file__).parent.parent / "configs"
    friday_config = ConfigParser()
    friday_config.read(__friday_config_dir / "ui_configs.ini")

    # Friday UI Assets
    __ui_assets_dir = Path(__file__).parent.parent / "assets" / "ui"
    logo_path = __ui_assets_dir / "icon.ico"

    # Appearance
    TITLE = friday_config["Friday"]["Title"]
    TOOL_MIN_WIDTH = friday_config["Friday"]["ToolMinWidth"]
    TOOL_MIN_HEIGHT = friday_config["Friday"]["ToolMinHeight"]
    TOOL_THEME = friday_config["Friday"]["ToolTheme"]

    # UI Constants
    FRAME_PAD = 5
    PROMPT_SEND_BUTTON_WIDTH = 100
    HEADER_FRAME_WIDGETS_PAD = 5
    PROMPT_FRAME_WIDGETS_PAD = 5
    CHAT_DISPLAY_FRAME_WIDGETS_PAD = 5
    APP_NAME = "FRIDAY"
    HEADER_FONT = ("Chiller", 25, "bold")
    CHAT_DISPLAY_FONT = ("Comic Sans MS", 15)


class HeaderFrame(customtkinter.CTkFrame):
    """Friday AI Personal Assistant User Interface Header Frame."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._add_widgets()

    def _add_widgets(self):
        """Add Widgets to Friday AI Personal Assistant User Interface Header Frame."""
        self.header_label = customtkinter.CTkLabel(
            self, text=FridayUIConstants.APP_NAME, font=FridayUIConstants.HEADER_FONT
        )
        self.header_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=FridayUIConstants.HEADER_FRAME_WIDGETS_PAD,
            pady=FridayUIConstants.HEADER_FRAME_WIDGETS_PAD,
        )

        switch_state = "on" if FridayUIConstants.TOOL_THEME == "dark" else "off"
        switch_var = customtkinter.StringVar(value=switch_state)
        self.dark_theme_switch = customtkinter.CTkSwitch(
            self,
            variable=switch_var,
            onvalue="on",
            offvalue="off",
            text="Dark Mode",
            font=FridayUIConstants.HEADER_FONT,
        )
        self.dark_theme_switch.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=FridayUIConstants.HEADER_FRAME_WIDGETS_PAD,
            pady=FridayUIConstants.HEADER_FRAME_WIDGETS_PAD,
        )


class PromptFrame(customtkinter.CTkFrame):
    """Friday AI Personal Assistant User Interface Prompt Frame."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._add_widgets()

    def _add_widgets(self):
        """Add Widgets to Friday AI Personal Assistant User Interface Prompt Frame."""
        self.prompt_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Enter prompt here...")
        self.prompt_entry.grid(
            row=0,
            column=0,
            padx=FridayUIConstants.PROMPT_FRAME_WIDGETS_PAD,
            pady=FridayUIConstants.PROMPT_FRAME_WIDGETS_PAD,
            sticky="nsew",
        )

        self.prompt_send_button = customtkinter.CTkButton(
            self, text="Send", width=FridayUIConstants.PROMPT_SEND_BUTTON_WIDTH
        )
        self.prompt_send_button.grid(
            row=0,
            column=1,
            padx=FridayUIConstants.PROMPT_FRAME_WIDGETS_PAD,
            pady=FridayUIConstants.PROMPT_FRAME_WIDGETS_PAD,
            sticky="nsew",
        )


class FridayChatDisplayFrame(customtkinter.CTkFrame):
    """Friday AI Personal Assistant User Interface Chat Display Frame."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._add_widgets()

    def _add_widgets(self):
        """Add Widgets to Friday AI Personal Assistant User Interface Chat Display Frame."""
        self.chat_display_text = customtkinter.CTkTextbox(
            self, state="disabled", wrap="word", font=FridayUIConstants.CHAT_DISPLAY_FONT
        )
        self.chat_display_text.grid(
            row=0,
            column=0,
            padx=FridayUIConstants.CHAT_DISPLAY_FRAME_WIDGETS_PAD,
            pady=FridayUIConstants.CHAT_DISPLAY_FRAME_WIDGETS_PAD,
            sticky="nsew",
        )


class FridayAPP(customtkinter.CTk):
    """Friday App User Interface built using CustomTkinter."""

    def __init__(self) -> None:
        super().__init__()
        self._friday_ui_configure()

        # Add Frames to Friday UI
        self.header_frame = HeaderFrame(master=self)
        self.header_frame.grid(
            row=0, column=0, padx=FridayUIConstants.FRAME_PAD, pady=FridayUIConstants.FRAME_PAD, sticky="nsew"
        )
        self.chat_display_frame = FridayChatDisplayFrame(master=self)
        self.chat_display_frame.grid(
            row=1, column=0, padx=FridayUIConstants.FRAME_PAD, pady=FridayUIConstants.FRAME_PAD, sticky="nsew"
        )
        self.prompt_frame = PromptFrame(master=self)
        self.prompt_frame.grid(
            row=2, column=0, padx=FridayUIConstants.FRAME_PAD, pady=FridayUIConstants.FRAME_PAD, sticky="nsew"
        )

        # Configure grid weights
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Bind Send Button
        self.prompt_frame.prompt_send_button.bind("<Button-1>", self._handle_send)

        # Bind Enter Key
        self.prompt_frame.prompt_entry.bind("<Return>", self._handle_send)

        # Bind Theme Switch
        self.header_frame.dark_theme_switch.bind("<Button-1>", self._handle_theme_switch)

        # Initialize Friday AI Personal Assistant
        self.friday = Friday()
        self.friday_chat = self.friday.google_ai_generation.start_new_chat()
        response = self.friday.google_ai_generation.generate_content(prompt="Who are you?")
        self._append_text_to_chat_display(text=f"Friday: {response.response.strip()}\n\n")

    def _friday_ui_configure(self):
        """Configure Friday AI Personal Assistant User Interface."""
        # Configure Friday UI
        self.title(FridayUIConstants.TITLE)
        self.iconbitmap(FridayUIConstants.logo_path)
        self.geometry(f"{FridayUIConstants.TOOL_MIN_WIDTH}x{FridayUIConstants.TOOL_MIN_HEIGHT}")
        self.minsize(int(FridayUIConstants.TOOL_MIN_WIDTH), int(FridayUIConstants.TOOL_MIN_HEIGHT))
        customtkinter.set_appearance_mode(mode_string=FridayUIConstants.TOOL_THEME)

    def _handle_send(self, event=None):
        """Handle the send button click or Enter key press."""
        text = self.prompt_frame.prompt_entry.get()
        if text.strip():
            self._append_text_to_chat_display(text=f"User: {text}\n")
            response = self._get_chat_response(user_input=text)
            if response:
                self._append_text_to_chat_display(text=f"Friday: {response}\n")
            else:
                self._append_text_to_chat_display(text=f"Friday: Apologize, Unable to process your request...\n")
            self._append_text_to_chat_display(text="\n")
            self.prompt_frame.prompt_entry.delete(0, "end")
            return "break"

    def _append_text_to_chat_display(self, text: str) -> None:
        """
        Append text to the chat display and scroll to the bottom.

        Args:
            text (str): Text to append to the chat display.
        """
        self.chat_display_frame.chat_display_text.configure(state="normal")
        self.chat_display_frame.chat_display_text.insert("end", text)
        self.chat_display_frame.chat_display_text.configure(state="disabled")
        # Scroll to the bottom
        self.chat_display_frame.chat_display_text.see("end")

    def _get_chat_response(self, user_input: str) -> str:
        """
        Get chat response from Friday AI Personal Assistant.

        Args:
            user_input (str): User input to send to Friday AI.

        Returns:
            str: Chat response from Friday AI.
        """
        try:
            response = self.friday.google_ai_generation.send_chat_message(chat=self.friday_chat, message=user_input)
        except FridayGenerationError:
            return ""
        return response.response.strip()

    def _handle_theme_switch(self, event=None):
        """Handle the theme switch."""
        switch_value = self.header_frame.dark_theme_switch.get()
        if switch_value == "on":
            customtkinter.set_appearance_mode(mode_string="dark")
        else:
            customtkinter.set_appearance_mode(mode_string="light")

    def run(self):
        """Run Friday AI Personal Assistant User Interface."""
        self.mainloop()


def main():
    friday_ui = FridayAPP()
    friday_ui.run()


if __name__ == "__main__":
    main()
