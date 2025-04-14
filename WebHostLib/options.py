from textwrap import dedent
from typing import Literal

from flask import Response, get_template_attribute, redirect, render_template
from flask_wtf import FlaskForm, Form
from typing_extensions import Self
from wtforms import FormField, SelectField, StringField, SubmitField, IntegerField, BooleanField, RadioField
from wtforms.widgets import NumberInput
from wtforms.validators import InputRequired, Optional

import Options
from Utils import local_path
from worlds.AutoWorld import AutoWorldRegister, World
from . import app, cache
from .generate import get_meta


class PlayerOptionsForm(FlaskForm):
    name = StringField(
        "Player Name",
        [InputRequired()],
        render_kw={"placeholder": "Player"},
        description="This is your unique player name for connecting from your game; also called your slot name.",
    )
    description = StringField("Options File Description", render_kw={"placeholder": "YAML Description"})
    submit_generate = SubmitField("Generate for Single Player")
    submit_export = SubmitField("Download Options")


# noinspection PyTypeChecker
class OptionField(FormField):
    SupportedType = Literal[
        "toggle",         # Toggle
        "choice",         # Choice
        "text",           # FreeText
        "text_choice",    # TextChoice
        "range",          # Range
        "named_range",    # NamedRange
        "keyed_list",     # OptionList or OptionSet w/ valid_keys
        "counter_dict"    # ItemDict
    ]

    def __init__(self, option_class: type[Options.Option], option_type: SupportedType, *args, **kwargs):
        self.option = option_class
        self.option_type = option_type

        super().__init__(*args, **kwargs)

    def __call__(self, **attrs) -> str:
        """Loads and returns the applicable HTML str for this option type when called."""
        return get_template_attribute("macros/options.jinja", f"option_{self.option_type}")(self, attrs)

    @classmethod
    def create(cls, world: type[World], option_name: str, option_class: type[Options.Option]) -> Self | None:
        """Attempt to instantiate a supported ``OptionField`` instance based on the type of option passed in.

        If the provided option is not supported, method will return ``None``.
        """
        # Load the appropriate help text for this option.
        if world.web.rich_text_options_doc or (world.web.rich_text_options_doc is None and option_class.rich_text_doc):
            description = cls.rst_to_html(getattr(option_class, "__doc__", ""))
        else:
            description = getattr(option_class, "__doc__", "").replace("\n    ", "\n")

        kwargs = {
            "label": getattr(option_class, "display_name", option_name),
            "description": description,
        }

        if issubclass(option_class, Options.TextChoice):
            return cls(option_class, "text_choice", cls._create_text_choice(option_name, option_class), **kwargs)
        if issubclass(option_class, Options.FreeText):
            return cls(option_class, "text", cls._create_text(option_name, option_class), **kwargs)
        if issubclass(option_class, Options.Toggle):
            return cls(option_class, "toggle", cls._create_toggle(option_name, option_class), **kwargs)
        if issubclass(option_class, Options.Choice):
            return cls(option_class, "choice", cls._create_choice(option_name, option_class), **kwargs)
        if issubclass(option_class, Options.NamedRange):
            return cls(option_class, "named_range", cls._create_range(option_name, option_class), **kwargs)
        if issubclass(option_class, Options.Range):
            return cls(option_class, "range", cls._create_range(option_name, option_class), **kwargs)

        # Unsupported option.
        return None

    @staticmethod
    def rst_to_html(text: str) -> str:
        """Converts reStructuredText (such as a Python docstring) to HTML."""
        from docutils.core import publish_parts

        if text.startswith(" ") or text.startswith("\t"):
            text = dedent(text)
        elif "\n" in text:
            lines = text.splitlines()
            text = lines[0] + "\n" + dedent("\n".join(lines[1:]))

        return publish_parts(
            text,
            writer_name="html",
            settings=None,
            settings_overrides={"raw_enable": False, "file_insertion_enabled": False, "output_encoding": "unicode"},
        )["body"]

    @classmethod
    def _create_text(cls, option_name: str, option_class: type[Options.FreeText]) -> type[Form]:
        form_class: type[Form] = type(f"{option_name}Form", (Form,), {})
        setattr(form_class, "value", StringField(default=option_class.default))

        return form_class

    @classmethod
    def _create_choice(cls, option_name: str, option_class: type[Options.Choice]) -> type[Form]:
        choices = [(key, option_class.get_option_name(id_)) for id_, key in option_class.name_lookup.items()]
        form_class: type[Form] = type(f"{option_name}Form", (Form, cls.RandomMixin), {})
        setattr(form_class, "value", SelectField(
            default=option_class.default,
            validators=[Optional()],
            choices=choices))

        return form_class

    @classmethod
    def _create_text_choice(cls, option_name: str, option_class: type[Options.TextChoice]) -> type[Form]:
        choices = [(key, option_class.get_option_name(id_)) for id_, key in option_class.name_lookup.items()]
        choices = [("", "-- Custom --")] + choices
        form_class: type[Form] = type(f"{option_name}Form", (Form, cls.RandomMixin), {})
        setattr(form_class, "value", SelectField(
            default=option_class.name_lookup.get(option_class.default, ""),
            validators=[Optional()],
            choices=choices))
        setattr(form_class, "custom_value", StringField(
            default=option_class.default if option_class.default not in option_class.name_lookup else "",
            validators=[Optional()],
            render_kw={"placeholder": "Custom input..."},
        ))

        return form_class

    @classmethod
    def _create_toggle(cls, option_name: str, option_class: type[Options.Toggle]) -> type[Form]:
        choices = [("true", "Yes"), ("false", "No")]
        form_class: type[Form] = type(f"{option_name}Form", (Form, cls.RandomMixin), {})
        setattr(form_class, "value", RadioField(
            default="true" if option_class.default else "false",
            validators=[Optional()],
            choices=choices))

        return form_class

    @classmethod
    def _create_range(cls, option_name: str, option_class: type[Options.Range]) -> type[Form]:
        form_class: type[Form] = type(f"{option_name}Form", (Form, cls.RandomMixin), {})
        setattr(form_class, "value", IntegerField(
            default=option_class.default,
            validators=[Optional()],
            widget=NumberInput(min=option_class.range_start, max=option_class.range_end)))

        return form_class

    class RandomMixin:
        random = BooleanField()


# Cached forms for each game, only created as needed.
_cached_forms: dict[str, type] = {}
_cached_groups: dict[str, dict[str, list[str]]] = {}

def get_player_options_form(world: type[World]) -> PlayerOptionsForm:
    if world.game in _cached_forms:
        return _cached_forms[world.game]()

    game_class = type("GameContainerForm", (Form,), {})
    groups: dict[str, list[str]] = {}
    for group_name, group_options in Options.get_option_groups(world, Options.Visibility.simple_ui).items():
        groups[group_name] = []
        for option_name, option_class in group_options.items():
            option_field = OptionField.create(world, option_name, option_class)
            if not option_field:
                continue

            groups[group_name].append(option_name)
            setattr(game_class, option_name, option_field)

        # Remove any empty groups from rendering by removing the group itself.
        if not groups[group_name]:
            del groups[group_name]

    form_class = type(f"{world.game}_PlayerOptionsForm", (PlayerOptionsForm,), {"game_options": FormField(game_class)})

    _cached_forms[world.game] = form_class
    _cached_groups[world.game] = groups
    return form_class()


@app.route("/games/<string:game>/options", methods=["GET"])
# @cache.cached()  # TODO: Remove cache before opening PR.
def get_player_options(game: str):
    world = AutoWorldRegister.world_types[game]
    if world.hidden or world.web.options_page is False:
        return redirect("games")

    form = get_player_options_form(world)

    return render_template(
        "options.html",
        game=world.game,
        theme=world.web.theme,
        form=form,
        groups=_cached_groups[world.game],
        getattr=getattr,
    )


@app.route("/games/<string:game>/options", methods=["POST"])
def post_player_options(game: str):
    import json

    world = AutoWorldRegister.world_types[game]
    if world.hidden or world.web.options_page is False:
        return redirect("games")

    form = get_player_options_form(world)

    if form.validate_on_submit():
        class SetEncoder(json.JSONEncoder):
            def default(self, obj):
                from collections.abc import Set

                if isinstance(obj, Set):
                    return list(obj)
                return json.JSONEncoder.default(self, obj)

        json_data = json.dumps(form.data, cls=SetEncoder)
        response = Response(json_data)
        response.headers["Content-Type"] = "application/json"
        return response

    return str(form.errors)


def create_options_files() -> None:
    import os

    target_folder = local_path("WebHostLib", "static", "generated")
    yaml_folder = os.path.join(target_folder, "configs")

    Options.generate_yaml_templates(yaml_folder)


def generate_game(options: dict[str, dict | str]) -> Response | str:
    from .generate import start_generation

    return start_generation(options, get_meta({}))


def send_yaml(options: dict) -> Response:
    import yaml

    response = Response(yaml.dump(options, sort_keys=False))
    response.headers["Content-Type"] = "text/yaml"
    response.headers["Content-Disposition"] = f"attachment; filename={options['name']}.yaml"
    return response


# TODO: Redirects that should be removed in AP 0.7.0
@app.route("/games/<string:game>/player-options")
def get_player_options_old(game: str):
    return redirect(f"/games/{game}/options", 301)


@app.route("/games/<string:game>/weighted-options")
def get_weighted_options_old(game: str):
    return redirect(f"/games/{game}/options", 301)


@app.route("/games/<string:game>/generate", methods=["POST"])
def post_options_generate(game: str):
    return redirect(f"/games/{game}/options", 308)


@app.route("/games/<string:game>/option-presets", methods=["GET"])
@cache.cached()
def option_presets(game: str) -> Response:
    import json

    world = AutoWorldRegister.world_types[game]

    presets = {}
    for preset_name, preset in world.web.options_presets.items():
        presets[preset_name] = {}
        for preset_option_name, preset_option in preset.items():
            if preset_option == "random":
                presets[preset_name][preset_option_name] = preset_option
                continue

            option = world.options_dataclass.type_hints[preset_option_name].from_any(preset_option)
            if isinstance(option, Options.NamedRange) and isinstance(preset_option, str):
                assert preset_option in option.special_range_names, (
                    f"Invalid preset value '{preset_option}' for '{preset_option_name}' in '{preset_name}'. "
                    f"Expected {option.special_range_names.keys()} or {option.range_start}-{option.range_end}."
                )

                presets[preset_name][preset_option_name] = option.value
            elif isinstance(option, (Options.Range, Options.OptionSet, Options.OptionList, Options.ItemDict)):
                presets[preset_name][preset_option_name] = option.value
            elif isinstance(preset_option, str):
                # Ensure the option value is valid for Choice and Toggle options
                assert option.name_lookup[option.value] == preset_option, (
                    f"Invalid option value '{preset_option}' for '{preset_option_name}' in preset '{preset_name}'. "
                    f"Values must not be resolved to a different option via option.from_text (or an alias)."
                )
                # Use the name of the option
                presets[preset_name][preset_option_name] = option.current_key
            else:
                # Use the name of the option
                presets[preset_name][preset_option_name] = option.current_key

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            from collections.abc import Set

            if isinstance(obj, Set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    json_data = json.dumps(presets, cls=SetEncoder)
    response = Response(json_data)
    response.headers["Content-Type"] = "application/json"
    return response
