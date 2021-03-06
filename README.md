

            ======================================================
            =               Survey Tool Prompt                   =
            ======================================================

            Requirements:
            1) Reads questions and answer choices from a JSON or plist file (samples input file and sample prompt outputs                   provided: sample_survey.json, sample_cli_prompts.txt).
            2) Presents multiple choice or free-form questions to the user and stores their responses.
            3) Writes user responses into a responses.json file. This file should accumulate responses as more people take the              survey, and it should track who gave each response.
            4) Should account for follow-up questions on certain multiple-choice responses (ie, if they choose a particular                 answer it might present a follow-up question).
            5) Include an extra script that aggregates responses and generates some type of report.
            6) Add support for N-deep nested follow-up questions (standard prompt only requires 1-level of follow-up questions).
