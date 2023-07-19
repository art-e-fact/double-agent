from double import extract_requirements


def test_extract_requirements():
    messages = [
        {
            "role": "system",
            "content": "RequirementsGPT. Your role is to help the user specfify full requirements for the web frontend of a project. The result should be enough to create an HTML template. Please prefix each requirement you will generate by REQ",
        },
        {
            "role": "assistant",
            "content": "Hello! How can I assist you today with your UI project requirements?",
        },
    ]
    requirements = extract_requirements(messages)
    assert requirements == ""
