import logging

from metasdk import MetaApp

log = MetaApp().log


def test_log_context(caplog):
    with caplog.at_level(logging.INFO):
        # Try log with context, without some set entities
        log.info("info_message_0", {"info_context_key_0": "info_context_value_0"})
        assert caplog.records[0].message == "info_message_0"
        assert caplog.records[0].msg == "info_message_0"
        assert caplog.records[0].context == {"info_context_key_0": "info_context_value_0"}

        # ...with one set entity
        log.set_entity("entity_key_1", "entity_value_1")
        log.info('info_message_1', {"info_context_key_1": "info_context_value_1"})
        assert caplog.records[1].message == "info_message_1"
        assert caplog.records[1].msg == "info_message_1"
        assert caplog.records[1].context == {"info_context_key_1": "info_context_value_1",
                                             "entity_key_1": "entity_value_1"}

        # ...change this entity value
        log.set_entity("entity_key_1", "entity_value_2")
        log.info('info_message_2', {"info_context_key_2": "info_context_value_2"})
        assert caplog.records[2].message == "info_message_2"
        assert caplog.records[2].msg == "info_message_2"
        assert caplog.records[2].context == {"info_context_key_2": "info_context_value_2",
                                             "entity_key_1": "entity_value_2"}

        # ...add one another entity
        log.set_entity("entity_key_3", "entity_value_3")
        log.info('info_message_3', {"info_context_key_3": "info_context_value_3"})
        assert caplog.records[3].message == "info_message_3"
        assert caplog.records[3].msg == "info_message_3"
        assert caplog.records[3].context == {"info_context_key_3": "info_context_value_3",
                                             "entity_key_1": "entity_value_2",
                                             "entity_key_3": "entity_value_3"}

        # ...remove first entity
        log.remove_entity("entity_key_1")
        log.info('info_message_4', {"info_context_key_4": "info_context_value_4"})
        assert caplog.records[4].message == "info_message_4"
        assert caplog.records[4].msg == "info_message_4"
        assert caplog.records[4].context == {"info_context_key_4": "info_context_value_4",
                                             "entity_key_3": "entity_value_3"}