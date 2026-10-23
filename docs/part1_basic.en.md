---
title: "Language basics"
capabilities: [language, compilation]
---

# Language basics

Nexa keeps Agent declarations, tools, and flow control in `.nx` files. The compiler normalizes an AST and generates Python. Declaration-only modules compile independently.

## Values and control flow

Assignment introduces variables. `result` is the flow return convention. Strings use double quotes, and statements may end in semicolons. This complete program returns `12` offline.

```nexa
flow main {
    first = 3;
    print(first * 4);
    result = first * 4;
}
```

Basic expressions include integers, floats, strings, Booleans, lists, maps, arithmetic, and comparisons. `if`, `for`, and `while` express deterministic control flow. Model-based semantic routing needs a configured model and explicit acceptance criteria.

## Agents and calls

An Agent's `prompt` defines instructions, `model` and `provider_api` select the model and protocol, and `uses` limits exposed tools. In this complete program, `run` initiates the model call.

```nexa
agent Echo {
    prompt: "Repeat the supplied text."
}

flow main {
    result = Echo.run("hello");
    verify result satisfies string;
}
```

Configure a [provider](runtime_providers.md), then execute with `uv run nexa run echo.nx`. The model should repeat the input; `verify` checks that its result is a string.

## Modules

`include "helpers.nxlib";` resolves relative to the importing file, then searches the packaged standard library. Each canonical path is imported once; cycle diagnostics include the dependency chain. `.nxs` files hold local configuration. Keep secret values out of examples and version control.

Continue with [Tools and Protocols](part3_extensions.md), [Advanced orchestration](part2_advanced.md), and [The compiler](part5_compiler.md).


## Branches

Deterministic `if` and `while` conditions use parentheses. Comparisons support `==`, `!=`, `>`, `>=`, `<`, and `<=`; combine conditions with `and` / `or`.

```nexa
flow main {
    value = 7;
    label = "";
    if (value > 5) {
        label = "large";
    } else {
        label = "small";
    }
    result = label;
}
```

This returns `large`. Finish a flow with a top-level assignment to make its return explicit. The current generator returns `None` for flows ending in `if`, `while`, or `print`.

## Collections and iteration

`for each item in items` iterates a collection. `for each index, item in items` supplies index and value. Array/map literal positions are limited in the current expression parser; construct collections through trusted `python!` code or tool results. `std.json.parse` returns the standard library's JSON text result; explicitly deserialize when a local Python collection is needed.

```nexa
flow main {
    python! """items = [1, 2, 3]"""
    total = 0;
    for each item in items {
        total = total + item;
    }
    result = total;
}
```

This returns `6`. `break;` exits the current loop; `continue;` advances to its next iteration.

## while loops

```nexa
flow main {
    counter = 0;
    while (counter < 3) {
        counter = counter + 1;
    }
    result = counter;
}
```

This returns `3`. Use [autoloop](part2_harness.md) to give autonomous model loops explicit step and time limits.

## Parameterized flows

Write parameters as `name: type` and the return type as `-> type`. Call a flow by name from another flow.

```nexa
flow double(value: int) -> int {
    result = value * 2;
}
flow main {
    result = double(6);
}
```

This returns `12`. See [Language reference](reference.md) for operators, types, and Agent parameters.

---

[Source and validation](capability_inventory.md) · `language` / `compilation`
