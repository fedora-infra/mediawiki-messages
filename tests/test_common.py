# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for common properties of the message schemas."""

from mediawiki_messages.article import ArticleEditV1

from .utils import DUMMY_ARTICLE_EDIT


def test_properties():
    """Assert some properties are correct."""
    message = ArticleEditV1(body=DUMMY_ARTICLE_EDIT)

    assert message.app_name == "Mediawiki"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/mediawiki.png"
    assert message.agent_name == "dummy-user"
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
    assert message.usernames == ["dummy-user"]
