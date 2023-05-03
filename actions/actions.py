# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import pandas as pd

# Load the data from the Excel file
df = pd.read_excel("database.xlsx")


import openpyxl
from rasa_sdk.events import SlotSet

class ActionQueryDatabase(Action):
    def name(self) -> Text:
        return "action_query_database"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the entity value from the tracker
        entity_value = tracker.latest_message['entities'][0]['value']
                
        # Search for the entity in a specific column of the dataframe
        # For example, if the entity is a name, search for it in the 'Student Name' column
        column_name = 'Student Name'
        row = df.loc[df[column_name] == entity_value]
        
        # Check if a matching row was found in the dataframe
        if row.empty:
            # If no matching row was found, inform the user and set the 'name' slot to False
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information for {entity_value}.")
            return [SlotSet('name', False)]
        
        else:
            # If a matching row was found, extract the information from a different column of the row
            # For example, if you want to extract the 'Student Name' column of the row, use the following code:
            info = row['Student ID'].values[0]
            message=f"The {entity_value} is {info}."
        
        # set the slot with the answer
        tracker.slots['name'] = message

        # return the response
        return [SlotSet("name", message), 
                dispatcher.utter_message(responses="utter_roll_no", name=message)]
            
            # # Inform the user of the extracted information and set the 'name' slot to True
            # dispatcher.utter_message(text=f"The {entity_value} capital is {info}.")
            # return [SlotSet('name', True)]















        # # Get the user's question from the tracker
        # user_question = tracker.latest_message['text']

        # # Open the Excel file
        # workbook = openpyxl.load_workbook('database.xlsx')

        # # Select the worksheet you want to query
        # worksheet = workbook['Sheet1']

        # # Loop through the rows in column "Student Name" to find the user's question
        # for cell in worksheet['Student Name']:
        #     if cell.value == entity_value:
        #         # Retrieve the answer from the same row in column 4 i.e "Student ID"
        #         answer = worksheet.cell(row=cell.row, column=4).value
        #         break
        # else:
        #     answer = "Sorry, I couldn't find the roll no. for the asked student."

        # # Set the answer as a slot value for future use
        # SlotSet("answer", answer)

        # # Send the answer back to the user
        # dispatcher.utter_message(text=f"The roll no. is: {answer}")

        # return [SlotSet("entity_value", entity_value)]



