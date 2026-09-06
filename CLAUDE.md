# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## Project Overview

This is an in-progress implementation of the **Lox** programming langauge interpreter from
the book *Crafting Interpreters*.

Dependencies are managed with `uv`. `ruff` is used with more than its default rules for
linting and formatting. The user is using the **helix** editor with the `ty` LSP.

## Guidance

1. Do not generate code unless the user explicitly asks for it - the purpose of this repository
    is to *learn*, not just finish the book.
2. When answering a conceptual question, include references to other programming languages like
    Python, JavaScript, or Rust where they would help.
3. Do not allude to later parts of the book than the user has said they're on unless explicitly
    necessary to answer a question - no spoilers.
4. The user will occassionally ask for verification of their implementation against their place
    in the book. Generate and run test case *without* saving them to the repo.
