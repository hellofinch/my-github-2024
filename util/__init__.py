from util.gh_fetch import get_github_info
import util.gh_filter as gh_filter
import util.gh_count as gh_count
import util.gh_sort as gh_sort
from log.logging_config import setup_logging

import json
import pytz
from datetime import timedelta, timezone as dt_timezone
import logging


setup_logging()


class Github:
    def __init__(
        self, access_token, username, timezone = "Asia/Shanghai"
    ):
        self.access_token = access_token
        self.username = username
        self.timezone = self._parse_timezone(timezone)
        self.data = None

    def _parse_timezone(self, tz_str):
        try:
            return pytz.timezone(tz_str)
        except pytz.UnknownTimeZoneError:
            if tz_str.startswith("+") or tz_str.startswith("-"):
                hours_offset = int(tz_str)
                timezone = dt_timezone(timedelta(hours=hours_offset))
                return pytz.timezone(timezone)
            else:
                raise ValueError(f"Invalid timezone format: {tz_str}")

    def fetch_data(self, year):
        self.data = get_github_info(self.username, self.access_token, self.timezone, year)
        return self

    def filter_data(self, filter_type, year):
        filter_func = getattr(gh_filter, f"{filter_type}_year")
        self.data = filter_func(self.data, year)
        return self

    def count_data(self, count_type):
        count_func = getattr(gh_count, f"{count_type}_number")
        self.data = count_func(self.data)
        return self

    def sort_data(self, sort_type, sort_by):
        sort_func = getattr(gh_sort, f"{sort_type}_{sort_by}")
        self.data = sort_func(self.data)
        return self

    def filter_all(self, year):
        for filter_type in ["commits", "issues", "prs"]:
            self.filter_data(filter_type, year)
        return self

    def filter_repos(self, year):
        self.filter_data("repos", year)
        return self

    def filter_json(self, key):
        self.data = gh_filter.json_key(self.data, key)
        return self

    def count_all(self):
        for count_type in [
            "commits",
            "commits_types",
            "commits_monthly",
            "commits_weekdaily",
            "commits_daily",
            "commits_hourly",
            "repos",
            "repos_languages",
            "repos_stargazer",
            "repos_fork",
            "prs",
            "prs_merged",
            "issues",
        ]:
            self.count_data(count_type)
        return self

    def sort_all(self):
        for sort_type, sort_by in [
            ("commits", "time"),
            ("repos", "time"),
            ("repos", "stargazer"),
            ("prs", "time"),
            ("issues", "time"),
        ]:
            self.sort_data(sort_type, sort_by)
        return self

    def read_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self

    def write_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.result, indent=4))
        return self

    def _get_result_structure(self, data):
        if isinstance(data, list):
            return [self._get_result_structure(data[0])]
        elif isinstance(data, dict):
            return {k: self._get_result_structure(v) for k, v in data.items()}
        else:
            return type(data).__name__

    def print_result_structure(self):
        logging.info(f"Result structure: ")
        return self

    @property
    def result(self):
        return self.data

    @result.setter
    def result(self, value):
        self.data = value
