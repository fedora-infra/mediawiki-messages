# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from mediawiki_messages.article import ArticleEditV1

from .utils import DUMMY_ARTICLE_EDIT


def test_minimal():
    """
    Assert the message schema validates a message with the required fields.
    """
    message = ArticleEditV1(body=DUMMY_ARTICLE_EDIT)
    message.validate()
    assert message.agent_name == "dummy-user"


def test_full():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = DUMMY_ARTICLE_EDIT.copy()
    body["diff_url"] = "http://localhost/wiki/diff"
    message = ArticleEditV1(body=body)
    message.validate()
    assert message.url == "http://localhost/wiki/diff"


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "summary": "This is a change",
        "title": "Page",
        "user": "dummy-user",
    }
    message = ArticleEditV1(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_str():
    """Assert __str__ produces a human-readable message."""
    expected_str = (
        "Wiki page Changes/Telemetry was edited by dummy-user\n"
        "Summary: This is a change\n"
        "Page: https://fedoraproject.org/wiki/Changes/Telemetry\n"
        "Diff: https://fedoraproject.org/w/index.php?title=Changes/Telemetry&diff=1&oldid=0\n"
    )
    message = ArticleEditV1(body=DUMMY_ARTICLE_EDIT)
    message.validate()
    assert expected_str == str(message)


def test_summary():
    """Assert the summary is correct."""
    expected_summary = "Wiki page Changes/Telemetry was edited by dummy-user"
    message = ArticleEditV1(body=DUMMY_ARTICLE_EDIT)
    assert expected_summary == message.summary


def test_user_page():
    """Assert we extract the username from the user page."""
    body = {
        "diff_url": "https://localhost/wiki/diff",
        "minor_edit": False,
        "page_url": "https://localhost/wiki/page",
        "summary": "This is a change",
        "title": "User:SomeUser",
        "user": "dummy-user",
    }
    message = ArticleEditV1(body=body)
    assert message.usernames == ["dummy-user", "someuser"]
