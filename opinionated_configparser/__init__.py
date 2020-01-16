import sys
import os

if sys.version_info[:2] < (3, 5):
    from backports import configparser
else:
    import configparser

try:
    from envtpl import render_string
except Exception:
    def render_string(*args, **kwargs):
        raise Exception("envtpl.render_string() not available")


MFCONFIG = os.environ.get("MFCONFIG", "GENERIC").lower()


def get_real_option(option):
    return option.split("[")[0]


def get_variant(option):
    if "[" not in option or "]" not in option:
        return None
    tmp = option.split("[")[1].split("]")[0]
    if len(tmp) == 0:
        return None
    return tmp


def get_score(variant, configuration_name):
    if variant == configuration_name:
        return sys.maxsize
    if variant is None:
        return 0.5
    tmp = configuration_name.split("_")
    if len(tmp) > 1:
        for i in range(len(tmp) - 1, 0, -1):
            tmp2 = "_".join(tmp[0:i])
            if variant == tmp2:
                return i
    return 0


class OpinionatedConfigParser(configparser.ConfigParser):
    def __init__(
        self,
        configuration_name=None,
        ignore_sections_starting_with="_",
        use_envtpl=False,
        envtpl_extra_variables={},
        envtpl_extra_search_paths=[],
        *args,
        **kwargs
    ):
        if configuration_name is not None:
            self.configuration_name = configuration_name.lower()
        else:
            self.configuration_name = MFCONFIG
        if "delimiters" not in kwargs:
            kwargs["delimiters"] = ("=",)
        if "comment_prefixes" not in kwargs:
            kwargs["comment_prefixes"] = ("#",)
        if "interpolation" not in kwargs:
            kwargs["interpolation"] = configparser.ExtendedInterpolation()
        if "default_section" in kwargs:
            # we can't use configparser default_section feature
            # so we will emulate later in the code
            self.__default_section = kwargs["default_section"]
        else:
            self.__default_section = None
        kwargs["default_section"] = None
        self.use_envtpl = use_envtpl
        self.envtpl_extra_variables = envtpl_extra_variables
        self.envtpl_extra_search_paths = envtpl_extra_search_paths
        self.ignore_sections_starting_with = ignore_sections_starting_with
        configparser.ConfigParser.__init__(self, *args, **kwargs)

    def read(self, *args, **kwargs):
        configparser.ConfigParser.read(self, *args, **kwargs)
        self._resolve_variant()

    def read_dict(self, *args, **kwargs):
        configparser.ConfigParser.read_dict(self, *args, **kwargs)
        self._resolve_variant()

    def read_string(self, *args, **kwargs):
        configparser.ConfigParser.read_string(self, *args, **kwargs)
        self._resolve_variant()

    def read_file(self, *args, **kwargs):
        configparser.ConfigParser.read_file(self, *args, **kwargs)
        self._resolve_variant()

    def _resolve_variant(self):
        def deal_with_option(tmp, read_section, write_section, option):
            real_option = get_real_option(option)
            variant = get_variant(option)
            score = get_score(variant, self.configuration_name)
            if score == 0:
                return
            if real_option in tmp[write_section]:
                if score <= tmp[write_section][real_option][0]:
                    # not better score
                    return
            value = self.get(read_section, option)
            if self.use_envtpl:
                value = render_string(
                    value,
                    die_on_missing_variable=False,
                    extra_variables=self.envtpl_extra_variables,
                    extra_search_paths=self.envtpl_extra_search_paths,
                )
            tmp[write_section][real_option] = (score, value)

        has_default = (
            self.__default_section is not None
            and self.__default_section in self.sections()
        )
        # first pass
        tmp = {}
        for section in self.sections():
            tmp[section] = {}
            for option in self.options(section):
                deal_with_option(tmp, section, section, option)
            if has_default:
                for option in self.options(self.__default_section):
                    deal_with_option(
                        tmp, self.__default_section, section, option
                    )
        # clear
        self.clear()
        # second pass
        for section in tmp.keys():
            if self.ignore_sections_starting_with and section.startswith(
                self.ignore_sections_starting_with
            ):
                continue
            for real_option in tmp[section].keys():
                value = tmp[section][real_option][1]
                if not self.has_section(section):
                    self.add_section(section)
                self.set(section, real_option, value)
