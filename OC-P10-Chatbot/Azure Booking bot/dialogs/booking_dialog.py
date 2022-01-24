# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult, waterfall_dialog
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.start_date_step,
                self.end_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step
                
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        #self.add_dialog(
        #    DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        #)
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options

        if booking_details.dst_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Can you please confirm to what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.dst_city)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.dst_city = step_context.result
        if booking_details.or_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Can you please confirm from what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.or_city)

    async def start_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for start travel date"""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.or_city = step_context.result
        if booking_details.str_date is None:          
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Can you please confirm when you wish start travelling ?")
                ),
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.str_date)

    async def end_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for end travel date"""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.str_date = step_context.result
        if booking_details.end_date is None:          
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Can you please confirm when wish to return ?")
                ),
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.end_date)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for end budget"""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.end_date = step_context.result
        if booking_details.budget is None:          
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Can you please confirm What would be your budget for this trip ?")
                ),
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.budget)

    

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options
       
        # Capture the results of the previous step
        booking_details.budget = step_context.result
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.dst_city }"
            f" from: { booking_details.or_city } departing: { booking_details.str_date} returing {booking_details.end_date} with a budget of {booking_details.budget} "
        )

        # Offer a YES/NO prompt.
        if booking_details.confirm is None:
            self.telemetry_client.track_trace(name="bot offered YES/NO prompt",properties={"message":"Bot offered YES/NO Prompt"},severity=1)
            self.telemetry_client.track_event(name="bot offered YES/NO prompt",properties={"message":"Bot offered YES/NO Prompt"})
            return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
            )
            
        return await step_context.next(booking_details.confirm)

        

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        booking_details = step_context.options
        entities={   "or_city":booking_details.or_city,
                    "dst_city":booking_details.dst_city,
                    "str_date":booking_details.str_date,
                    "end_date":booking_details.end_date,
                    "budget":booking_details.budget  }
        
        
        self.telemetry_client.track_trace(name="user confirmation",properties={"confirmation_value":step_context.result,
                                                                                "or_city":booking_details.or_city,
                                                                                "dst_city":booking_details.dst_city,
                                                                                "str_date":booking_details.str_date,
                                                                                "end_date":booking_details.end_date,
                                                                                "budget":booking_details.budget})

        if step_context.result:
            booking_details = step_context.options
            booking_details.confirm = step_context.result

            return await step_context.end_dialog(booking_details)

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
