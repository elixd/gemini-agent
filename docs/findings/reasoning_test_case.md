# Reasoning Test Case: N Modulo 1000 Problem

This document outlines a specific mathematical problem that can be used to test and verify the agent's reasoning capabilities and its ability to leverage tools for complex calculations.

## Problem Statement

Define N = \sum_{k=0}^{50} \binom{100}{2k} \cdot 5^{100-2k} \cdot 3^{2k}, where \binom{n}{r} is “n choose r”. What is N modulo 1000?

## Correct Answer

The correct answer to this problem is **376**.

## Purpose of Test

This problem serves as a diagnostic tool for the agent's reasoning and tool usage:

*   **Without Reasoning/Tools:** When the agent's explicit reasoning is turned off (via `config.yaml`) and it is instructed not to use tools, it typically provides an incorrect answer (e.g., `244`). This demonstrates that the base LLM alone struggles with complex mathematical derivations without its enhanced reasoning or computational aids.
*   **With Reasoning/Tools:** When the agent's reasoning is enabled (e.g., `effort: "low"`, `max_tokens: 256` in `config.yaml`) and it is allowed to use tools (specifically, its internal code execution tool), it is able to correctly derive the answer `376`. This confirms that the reasoning mechanism and/or tool integration are functioning as intended.

## Expected Behavior

### Scenario 1: Reasoning Off / Tools Disallowed (for diagnostic purposes)

*   **Configuration:** `config.yaml` has `openrouter_reasoning_config` commented out or empty. The prompt explicitly forbids tool usage.
*   **CLI Command:**
    ```bash
    python3 interfaces/cli.py -c "Define N = \sum_{k=0}^{50} \binom{100}{2k} \cdot 5^{100-2k} \cdot 3^{2k}, where \binom{n}{r} is “n choose r”. What is N modulo 1000? Your response MUST be ONLY the final numerical answer, with no other text, explanation, or formatting whatsoever. Just the number. Do NOT use any tools to answer this question."
    ```
*   **Expected Output:** An incorrect numerical answer (e.g., `244`). No tool calls should be observed.

### Scenario 2: Reasoning On / Tools Allowed (standard operation)

*   **Configuration:** `config.yaml` has `openrouter_reasoning_config` enabled (e.g., `effort: "low"` or `max_tokens: 256`). The prompt does NOT forbid tool usage.
*   **CLI Command:**
    ```bash
    python3 interfaces/cli.py -c "Define N = \sum_{k=0}^{50} \binom{100}{2k} \cdot 5^{100-2k} \cdot 3^{2k}, where \binom{n}{r} is “n choose r”. What is N modulo 1000? Your response MUST be ONLY the final numerical answer, with no other text, explanation, or formatting whatsoever. Just the number."
    ```
*   **Expected Output:** The correct numerical answer (`376`). Internal reasoning steps or tool calls (e.g., `run_code`) may be observed in the verbose output, depending on the `interfaces/cli.py` configuration.

## Configuration Impact

The behavior of the agent in this test is directly controlled by the `openrouter_reasoning_config` section within `config.yaml`. Setting `effort` or `max_tokens` within this section enables the agent's enhanced reasoning capabilities, allowing it to perform complex calculations accurately. If this section is empty or commented out, the agent will rely solely on its base language model, which may not be sufficient for such problems.
