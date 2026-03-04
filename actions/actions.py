# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionSubmitTarot(Action):
    """塔罗表单填完后：读出 slot 并回复确认（带记忆）。"""

    def name(self) -> Text:
        return "action_submit_tarot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        question = tracker.get_slot("question") or "（未说）"
        spread_type = tracker.get_slot("spread_type") or "（未选）"
        dispatcher.utter_message(
            text=f"好的，您问的是「{question}」，用「{spread_type}」来占。稍后给您解读～"
        )
        return []
