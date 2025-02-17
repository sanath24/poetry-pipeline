from typing import Union, List

import replicate


class ParrotPromptCreator:
    def __init__(self):
        self.model = replicate.models.get("kyrick/prompt-parrot").versions.get("7349c6ce7eb83fc9bc2e98e505a55ee28d7a8f4aa5fb6f711fad18724b4f2389")

    def generate_prompt(self,
                        parsed_text: Union[List[List[str]], List[str]],
                        *,
                        prompt_by_stanza: bool = False,
                        lines_per_prompt: int = 2
                        ) -> List[str]:
        """
        Creates prompts naively (doesn't do any sort of processing at all. Mostly for POC)

        :param parsed_text: the parsed text
        :param prompt_by_stanza: creates prompt at stanza level if True
        :param lines_per_prompt: number of lines to use per prompt
        :return: generated prompts
        """
        if not isinstance(parsed_text[0], list) and prompt_by_stanza:
            raise ValueError('expected parsed_text to be List[List[str]] if prompt_by_stanza')

        prompts = []
        n = lines_per_prompt
        # case where we generate multiple prompts per stanza
        if isinstance(parsed_text[0], list) and not prompt_by_stanza:
            for stanza in parsed_text:
                stanza_prompts = ['\n'.join(stanza[i * n: (i + 1) * n]) for i in range((len(stanza) + n - 1) // n)]
                prompts += stanza_prompts
        # case where we generate single prompt per stanza
        elif isinstance(parsed_text[0], list) and prompt_by_stanza:
            prompts = ['\n'.join(stanza) for stanza in parsed_text]
        # case where we generate prompts by line
        elif not isinstance(parsed_text[0], list):
            prompts = ['\n'.join(parsed_text[i * n: (i + 1) * n]) for i in range((len(parsed_text) + n - 1) // n)]

        for i, prompt in enumerate(prompts):
            prompts[i] = prompt.lower()

        for i, prompt in enumerate(prompts):
            returned_prompts = self.model.predict(prompt=prompt)
            model_output = returned_prompts.split("\n------------------------------------------\n")
            prompts[i] = model_output[0]

        return prompts



