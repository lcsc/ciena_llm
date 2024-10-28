from langchain_ollama import OllamaLLM

# Configuration dictionary containing default and stage-specific settings
config = {
    "default": {
        "name": "llama3.1:8b",
        "temperature": 0,
        "context_length": 32768,
        "num_predict_tokens": 100,
    }
}

# Stage name
stage = "test_stage"

# Retrieve default and stage-specific configuration and merge them
default_config = config.get("default", {})
stage_config = config.get(stage, {})
merged_config = {**default_config, **stage_config}

llm_name = merged_config["name"]
llm_temperature = merged_config["temperature"]
llm_context_length = merged_config["context_length"]
llm_num_predict_tokens = merged_config["num_predict_tokens"]

# Initialize the appropriate backend LLM
backend_name = merged_config.get("backend", "ollama")
if backend_name == "ollama":
    llm = OllamaLLM(
        model=llm_name,
        temperature=llm_temperature,
        num_ctx=llm_context_length,
        num_predict=llm_num_predict_tokens,
    )
else:
    raise ValueError(f"Unsupported backend: {backend_name}")


def check_context_length(text):
    """
    Check if the context length of the full prompt exceeds the LLM's context length.

    :param text: The full prompt text.
    """
    num_tokens_full_prompt = llm.get_num_tokens(text)

    print(
        "Num. tokens (full prompt / max. context length): %s / %s"
        % (
            num_tokens_full_prompt,
            llm_context_length,
        )
    )
    if num_tokens_full_prompt > llm_context_length:
        raise ValueError("Full prompt exceeds context length.")


# Example prompt that will generate a very long text
prompt = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc accumsan sodales lectus in tempor. Nunc ipsum neque, pretium at libero eget, tempor tincidunt lorem. In pretium aliquam est vel accumsan. Curabitur efficitur vehicula sapien a dictum. Curabitur ultrices commodo ipsum sit amet pharetra. Nulla congue, nisi ac venenatis placerat, ligula nulla blandit nibh, id iaculis erat elit ut justo. Morbi egestas leo et odio efficitur, vel molestie neque scelerisque. Aenean augue justo, tincidunt nec neque sed, consectetur ultrices mi. Donec commodo, ligula vel porttitor tincidunt, magna magna porttitor lorem, et tincidunt enim arcu nec augue.

Etiam vitae ligula non sapien viverra suscipit. Duis non volutpat enim, eu lacinia leo. Aliquam pharetra dui in massa dignissim imperdiet. Integer luctus ante tellus, ac venenatis nisl sollicitudin ac. Cras vitae libero a diam euismod luctus. Interdum et malesuada fames ac ante ipsum primis in faucibus. In hac habitasse platea dictumst. Donec sagittis, nulla tristique fermentum ornare, lorem velit fringilla tortor, ut eleifend nunc metus ac sapien.

Aenean volutpat aliquam elementum. Phasellus vel tortor volutpat, efficitur elit non, tincidunt arcu. Maecenas sodales tempus blandit. Pellentesque aliquam auctor dictum. Vestibulum quis euismod lacus, nec aliquet augue. Suspendisse eu bibendum tellus. Morbi imperdiet pretium porttitor. Cras convallis malesuada est laoreet commodo. Praesent nulla justo, iaculis in egestas ac, gravida eget augue. Nulla porttitor porta turpis, facilisis euismod enim rhoncus vitae. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi eget nisl interdum, ornare tortor at, laoreet elit. Integer tincidunt nisi sed augue vulputate condimentum. Donec vitae turpis neque. Etiam tincidunt augue tellus, ac pharetra lacus rutrum ac. Nullam ante massa, finibus eu bibendum sit amet, imperdiet nec ante.

Donec dignissim felis sit amet turpis auctor rhoncus at a risus. Morbi euismod aliquet metus, at maximus mi placerat sed. Vestibulum iaculis sagittis orci semper vestibulum. Donec leo nisi, tincidunt ac tincidunt at, commodo a est. Nulla ut vestibulum elit, sollicitudin dignissim elit. Sed porta molestie metus, sed luctus risus. Nunc gravida diam vel cursus porttitor. Duis commodo tincidunt aliquet. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed facilisis, justo eget tincidunt tincidunt, quam lectus sagittis nunc, a venenatis diam purus quis diam. Curabitur vitae ipsum varius, luctus nibh at, iaculis ex. Nulla facilisi. Vivamus vel quam ac est cursus auctor vel sed lectus. Quisque nulla odio, dignissim quis consequat pharetra, pellentesque non nisl.

Pellentesque luctus est mi, vitae cursus ex porttitor a. Aenean imperdiet, orci lobortis dictum semper, leo dolor laoreet neque, vel convallis lectus nisi at tortor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras congue porta enim, sit amet maximus est vehicula sed. Curabitur condimentum vulputate gravida. Phasellus tempus auctor nulla, lacinia ultricies felis sollicitudin sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nam blandit sollicitudin blandit. Vestibulum eu egestas augue, sed bibendum nibh. Curabitur consequat eget lacus eu mollis. Aenean auctor sed eros vel interdum. Aliquam erat nunc, pretium eget velit in, pulvinar hendrerit nunc. Nunc malesuada condimentum sagittis. Aenean libero felis, ultricies et eros id, suscipit pretium risus. Praesent nec urna eu leo laoreet rutrum. In ultricies aliquam eros, sit amet auctor ipsum tincidunt ut.
"""

# Check context length before calling LLM
check_context_length(prompt)

# Print input before calling LLM
print(f"Input to LLM ({stage}): {prompt}")

# Call the LLM with the input text using the `invoke` method
response = llm.invoke(prompt)

# Print output after LLM call
print(f"Output from LLM ({stage}): {response}")

check_context_length(response)
