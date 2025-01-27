# summarize_chat_relationship_v2.py

import traceback
from pydantic import BaseModel

from ..common import openai_config
from ..gpt_structure import generate_prompt, ChatGPT_safe_generate_structured_response

# Variables:
# !<INPUT 0>! -- Statements
# !<INPUT 1>! -- curr persona name
# !<INPUT 2>! -- target_persona.scratch.name

template = """
[Statements]
!<INPUT 0>!

Based on the statements above, summarize !<INPUT 1>! and !<INPUT 2>!'s relationship. What do they feel or know about each other?
"""


class ChatSummarizeRelationship(BaseModel):
  summary: str


def run_gpt_prompt_agent_chat_summarize_relationship(
  persona, target_persona, statements, test_input=None, verbose=False
):
  def create_prompt_input(persona, target_persona, statements, test_input=None):
    prompt_input = [statements, persona.scratch.name, target_persona.scratch.name]
    return prompt_input

  # def __func_clean_up(gpt_response: ChatSummarizeRelationship, prompt=""):
  #   return gpt_response.summary

  # def __func_validate(gpt_response, prompt=""):
  #   try:
  #     if not isinstance(gpt_response, ChatSummarizeRelationship):
  #       return False
  #     __func_clean_up(gpt_response, prompt)
  #     return True
  #   except:
  #     traceback.print_exc()
  #     return False

  def get_fail_safe():
    return "..."

  # ChatGPT Plugin ===========================================================
  def __chat_func_clean_up(
    gpt_response: ChatSummarizeRelationship, prompt=""
  ):  ############
    return gpt_response.summary

  def __chat_func_validate(gpt_response, prompt=""):  ############
    try:
      if not isinstance(gpt_response, ChatSummarizeRelationship):
        return False
      __chat_func_clean_up(gpt_response, prompt)
      return True
    except:
      traceback.print_exc()
      return False

  print("DEBUG 18")  ########
  gpt_param = {
    "engine": openai_config["model"],
    "max_tokens": 200,
    "temperature": 0,
    "top_p": 1,
    "stream": False,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": None,
  }
  prompt_input = create_prompt_input(persona, target_persona, statements)  ########
  prompt = generate_prompt(prompt_input, prompt_template_str=template)
  example_output = "Jane Doe is working on a project"  ########
  special_instruction = (
    "The output should be a string that responds to the question."  ########
  )
  fail_safe = get_fail_safe()  ########
  output = ChatGPT_safe_generate_structured_response(
    prompt,
    ChatSummarizeRelationship,
    example_output,
    special_instruction,
    3,
    fail_safe,
    __chat_func_validate,
    __chat_func_clean_up,
    True,
  )
  if output != False:
    return output, [output, prompt, gpt_param, prompt_input, fail_safe]

  # ChatGPT Plugin ===========================================================

  # gpt_param = {"engine": openai_config["model"], "max_tokens": 150,
  #              "temperature": 0.5, "top_p": 1, "stream": False,
  #              "frequency_penalty": 0, "presence_penalty": 0, "stop": None}
  # prompt_template = "persona/prompt_template/v2/summarize_chat_relationship_v1.txt"
  # prompt_input = create_prompt_input(persona, target_persona, statements)
  # prompt = generate_prompt(prompt_input, prompt_template)

  # fail_safe = get_fail_safe()
  # output = safe_generate_response(prompt, gpt_param, 5, fail_safe,
  #                                  __func_validate, __func_clean_up)

  # if debug or verbose:
  #   print_run_prompts(prompt_template, persona, gpt_param,
  #                     prompt_input, prompt, output)

  # return output, [output, prompt, gpt_param, prompt_input, fail_safe]
