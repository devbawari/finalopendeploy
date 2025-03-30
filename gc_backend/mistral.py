import asyncio
import json
import os
import time
from mistralai import Mistral, UserMessage, Tool


prompt = [
    {
        "role": "system",
        "content":
        """
You are an AI-powered HR assistant designed to help employees manage stress by engaging in natural, supportive conversations. Your goal is to determine the root cause of stress by asking appropriate follow-up questions based on the user's responses.

You have access to an API key that allows you to retrieve past employee interactions, workload data, feedback history, and common stress indicators.

Behavioral Flow:

Start with an open-ended question to gauge the employee's current state.

Analyze their response using available historical data and context.

Determine the most relevant follow-up question based on their answer.

Continue adapting questions dynamically until a root cause is identified.

Offer personalized recommendations or escalate concerns if necessary.

Example API Call Flow:

User Input: "I feel overwhelmed lately."

API Request: Retrieve past workload and feedback history.

AI Decision: If past data shows high workload, ask: "Is your current workload heavier than usual, or are there other factors causing stress?"

User Input: "Too many deadlines."

API Request: Fetch deadline patterns from past data.

AI Decision: If deadlines frequently cause stress, ask: "Would it help if I suggest better task prioritization strategies?"

Ensure each question is empathetic, context-aware, and progressively narrows down the root cause while maintaining a confidential and supportive tone.

User Past Data:-
{'Index': np.int64(8), 'Employee_ID': 'EMP0009', 'Teams_Messages_Sent_sum': np.float64(44.0), 'Teams_Messages_Sent_mean': np.float64(22.0), 'Teams_Messages_Sent_median': np.float64(22.0), 'Teams_Messages_Sent_std': np.float64(31.11269837220809), 'Emails_Sent_sum': np.float64(50.0), 'Emails_Sent_mean': np.float64(25.0), 'Emails_Sent_median': np.float64(25.0), 'Emails_Sent_std': np.float64(1.4142135623730951), 'Meetings_Attended_sum': np.float64(2.0), 'Meetings_Attended_mean': np.float64(1.0), 'Meetings_Attended_median': np.float64(1.0), 'Meetings_Attended_std': np.float64(1.4142135623730951), 'Work_Hours_sum': np.float64(16.28), 'Work_Hours_mean': np.float64(8.14), 'Work_Hours_median': np.float64(8.14), 'Work_Hours_std': np.float64(1.3010764773832482), 'Last_activity_entry': '2024-02-25', 'Total_activity_entry': np.float64(2.0), 'Annual_Leave_Factor': np.float64(0.0), 'Casual_Leave_Factor': np.float64(9.01650989516398), 'Sick_Leave_Factor': np.float64(0.0), 'Unpaid_Leave_Factor': np.float64(0.0), 'Joining_Date': '2023-08-31', 'Onboarding_Feedback': 'Average', 'Mentor_Assigned': np.True_, 'Initial_Training_Completed': np.False_, 'Days_Since_Joining': np.float64(257.0), 'Onboarding_Factor': np.float64(0.0765355454239115), 'Performance_Rating': np.float64(1.0), 'Manager_Feedback': 'Meets Expectations', 'Promotion_Consideration': np.True_, 'Last_Review_Period': 'H2', 'Last_Review_Year': np.float64(2023.0), 'Best_Team_Player_Count': np.float64(2.0), 'Innovation_Award_Count': np.float64(0.0), 'Leadership_Excellence_Count': np.float64(1.0), 'Star_Performer_Count': np.float64(1.0), 'Total_Decayed_Reward_Points': np.float64(74.64253822558632), 'Decayed_Emotion_Zone': np.float64(-0.3671984580554357), 'Decayed_Vibe': np.float64(0.7343969161108714)}
"""
    }
]


async def main():
    client = Mistral(
        api_key='Z8c1IRM576ryQOUkfjDul7GeShQ37ULN',
    )
    while 1:
        query = input("Enter you query\n")
        user_prompt = {"role": "user", "content": query}
        new_prompt = prompt
        new_prompt.append(user_prompt)
        messages = new_prompt
        # Or using the new message classes
        # messages = [
        #     UserMessage(
        #         content="What is the best French cheese?",
        #     ),
        # ]
        # start = time.time()
        async_response = await client.chat.stream_async(
            messages=messages,
            model="mistral-large-latest"
            # tools=tools
        )

        async for chunk in async_response:
            print(chunk.data.choices[0].delta.content, end="")
            # response_text += chunk_text
            # print(chunk_text, end="")

        # print(f"\nResponse Time: {response_time:.2f} seconds")

        # Check if Mistral wants to call a function
        # try:
        # print(chunk.data.choices[0])
        # try:
        #     if hasattr(chunk.data.choices[0].delta, "tool_calls"):
        #         tool_call = chunk.data.choices[0].delta.tool_calls[0]
        #         function_name = tool_call.function.name
        #         function_args = json.loads(tool_call.function.arguments)

        #         print(f"Mistral wants to call function: {function_name}")
        #         print(f"Arguments: {function_args}")

        #         # Execute the PIN validation function
        #         if function_name == "pin_function":
        #             pin_result = pin_function(function_args["pin"])
        #             print("🔑 PIN Validation Result:", pin_result)
        #         # chunk = None
        # except:
        #     pass
        print()

asyncio.run(main())
