import logging

from _pytest.logging import LogCaptureFixture

from metasdk import MetaApp

log = MetaApp().log


def assert_and_clear_caplog(caplog: LogCaptureFixture, asserted_msg: str, asserted_context: dict):
    """Assert first (zero) record in caplog, than clear it"""

    assert caplog.records[0].message == asserted_msg
    assert caplog.records[0].msg == asserted_msg
    assert caplog.records[0].context == asserted_context

    caplog.clear()


def test_log_entity(caplog):
    #TODO Refactor it (automate duplicated parts)
    #TODO Add test for error log level
    with caplog.at_level(logging.INFO):
        # Try log with context, without some set entities
        log.info("info_message_0", {"info_context_key_0": "info_context_value_0"})
        assert_and_clear_caplog(caplog, "info_message_0", {"info_context_key_0": "info_context_value_0"})

        # ...with one set entity
        log.set_entity("entity_key_1", "entity_value_1")
        log.info('info_message_1', {"info_context_key_1": "info_context_value_1"})
        assert_and_clear_caplog(caplog,
                                "info_message_1",
                                {"info_context_key_1": "info_context_value_1",
                                 "entity_key_1": "entity_value_1"})

        # ...change this entity value
        log.set_entity("entity_key_1", "entity_value_2")
        log.info('info_message_2', {"info_context_key_2": "info_context_value_2"})
        assert_and_clear_caplog(caplog,
                                "info_message_2",
                                {"info_context_key_2": "info_context_value_2",
                                 "entity_key_1": "entity_value_2"})

        # ...add one another entity
        log.set_entity("entity_key_3", "entity_value_3")
        log.info('info_message_3', {"info_context_key_3": "info_context_value_3"})
        assert_and_clear_caplog(caplog,
                                "info_message_3",
                                {"info_context_key_3": "info_context_value_3",
                                 "entity_key_1": "entity_value_2",
                                 "entity_key_3": "entity_value_3"})

        # ...remove first entity
        log.remove_entity("entity_key_1")
        log.info('info_message_4', {"info_context_key_4": "info_context_value_4"})
        assert_and_clear_caplog(caplog,
                                "info_message_4",
                                {"info_context_key_4": "info_context_value_4",
                                 "entity_key_3": "entity_value_3"})
